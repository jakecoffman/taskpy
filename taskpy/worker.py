from celery import Celery
import subprocess
import datetime
import tempfile
import time
import re

from taskpy.models.run import RunResult

celery = Celery('taskpy-worker', broker='amqp://guest@localhost//', backend='amqp')

@celery.task
def run_job(config):
	result = RunResult()
	result.record_begin()
	success = True
	for task in config.tasks:
		process = subprocess.Popen([task['script_path']], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		output = process.communicate()[0]
		rcode = process.wait()
		result.record_task(task['name'], output, rcode)
		if rcode != 0:
			success = False
			break
	result.record_end(success)
	return result.as_json()
