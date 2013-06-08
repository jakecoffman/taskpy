from celery import Celery
import subprocess
import tempfile
import stat
import os

from taskpy.models.run import RunResult
from taskpy.models import db, Run

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
		result.record_task(task['name'], output, rcode)
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
	db.session.commit()
