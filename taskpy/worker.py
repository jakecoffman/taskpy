from flask import current_app as app
from celery import Celery
import subprocess
import tempfile
import stat
import os

from taskpy.models.run import RunResult
from taskpy.models import db, Run, TaskResult

celery = Celery('taskpy-worker', broker='amqp://guest@localhost//', backend='amqp')

@celery.task
def run_job(config):
	result = RunResult(celery_id=run_job.request.id)
	result.record_begin()
	success = True
	for task in config.tasks:
		# Write script to disk
		script = tempfile.NamedTemporaryFile(prefix='taskpy_script_{}_'.format(task['name']), delete=False)
		script.write(task['script'])
		script.close()
		# Executable permissions
		os.chmod(script.name, stat.S_IRWXU)
		# Run the script, capturing the output
		process = subprocess.Popen([script.name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		output = process.communicate()[0]
		rcode = process.wait()
		# Delete temp file
		os.remove(script.name)
		result.record_task(task['id'], output, rcode)
		if rcode != 0:
			success = False
			break
	result.record_end(success)
	return result

@celery.task
def record_results(results):
	run = db.session.query(Run).filter(Run.celery_id==results.celery_id).one()
	run.start_time = results.start_time
	run.end_time = results.end_time
	run.result = results.state

	# Record individual task output
	parent = None
	log_dir = os.path.join(app.config['TASKPY_BASE'], 'results')
	if not os.path.exists(log_dir):
		os.mkdir(log_dir)
	for task in results.tasks:
		r = TaskResult()
		r.run_id = run.id
		r.parent_id = parent
		r.task_id = task['task_id']
		r.return_code = task['return_code']
		r.end_time = task['end_time']
		r.start_time = results.start_time

		# Output log file
		log_file = tempfile.NamedTemporaryFile(prefix='result_', suffix='.log', dir=log_dir, delete=False)
		log_file.write(task['output'])
		r.log_file = log_file.name

		db.session.add(r)
		parent = r.id

	# Commit to database
	db.session.commit()
