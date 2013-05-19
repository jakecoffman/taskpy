import json
import os
import shutil
import time
import glob
import datetime
import iso8601
import flask
import subprocess
import tempfile

import taskpy.models.tasks as task_list

class Configuration(object):
	def __init__(self, base_dir):
		self.base_dir = base_dir
		self.jobs = {}
		self.tasks = {}
		self.load()

	def load(self):
		'''
		De-serialize the objects form the files.

		NOTE: We must load the tasks first, because the jobs reference them.
		'''
		tasks_json = self.load_file(os.path.join(self.base_dir, 'tasks.json'))
		self.load_tasks(tasks_json)
		jobs_json = self.load_file(os.path.join(self.base_dir, 'jobs.json'))
		self.load_jobs(jobs_json)

	def load_file(self, filename):
		if not os.path.exists(filename):
			return dict()
		with open(filename, 'r') as fle:
			return json.load(fle)

	def load_jobs(self, json_data):
		for name, data in json_data.iteritems():
			self.jobs[name] = Job( name=name
								 , data=data
								 , configuration=self
								 )

	def load_tasks(self, json_data):
		for name, data in json_data.iteritems():
			self.tasks[name] = Task( name=name
								   , data=data
								   , configuration=self
								   )

	def save(self):
		if not os.path.exists(self.base_dir):
			os.makedirs(self.base_dir)
		jobs_data = {job.name: job.as_json() for _, job in self.jobs.items()}
		tasks_data = {name: task.as_json() for name, task in self.tasks.items()}
		with open(os.path.join(self.base_dir, 'jobs.json'), 'w') as fle:
			json.dump(jobs_data, fle)
		with open(os.path.join(self.base_dir, 'tasks.json'), 'w') as fle:
			json.dump(tasks_data, fle)

	def add(self, obj):
		if isinstance(obj, Job):
			self.jobs[obj.name] = obj
		if isinstance(obj, Task):
			self.tasks[obj.name] = obj

	def remove(self, obj):
		if isinstance(obj, Job):
			self.jobs.pop(obj.name)
		if isinstance(obj, Task):
			self.tasks.pop(obj.name)

class Job(object):
	def __init__(self, name, configuration, data={}):
		self.name = name
		self.tasks = [configuration.tasks.get(x) for x in data.get('tasks', [])]
		self.runs = [Run(self, x, configuration) for x in data.get('runs', [])]
		self.configuration = configuration

	def as_json(self):
		return  { 'name': self.name
				, 'tasks': [x.name for x in self.tasks]
				, 'runs': [x.as_json() for x in self.runs]
				}

	def update_tasks(self, tasks):
		self.tasks = [self.configuration.tasks.get(x) for x in tasks]

	@property
	def status(self):
		if self.runs:
			return self.runs[-1].status
		return None

	@property
	def last_run(self):
		if self.runs:
			return self.runs[-1].start_time
		return None

	@property
	def folder(self):
		return os.path.join(self.configuration.base_dir, 'jobs', self.name)

	def run(self):
		this_run = Run(self, {})
		self.runs.append(this_run)
		this_run.run()

class Run(object):
	def __init__(self, job, data):
		self.job = job
		self.state = data.get('state', None)
		self.log_filename = data.get('log_filename', None)
		self.start_time = self.load_time(data, 'start_time')
		self.end_time = self.load_time(data, 'end_time')

	def load_time(self, data, field):
		'''Unserialize the string formatted time into datetime.datetime'''
		if field in data:
			return iso8601.parse_date(data.get(field))
		return None

	def run(self):
		if not os.path.exists(self.job.folder):
			os.makedirs(self.job.folder)
		log_file = tempfile.NamedTemporaryFile(suffix='.log', prefix='run_', dir=self.job.folder, delete=False)
		self.log_filename = log_file.name
		self.start_time = datetime.datetime.utcnow()
		self.state = 'running'
		status = True
		for task in self.job.tasks:
			log_file.write('Starting task "{0}" at {1}\n'.format(task.name, datetime.datetime.utcnow().isoformat()))
			status = task.run(log_file)
			if not status:
				break
		self.state = ('failed', 'success')[status]
		self.end_time = datetime.datetime.utcnow()

	def as_json(self):
		'''Serialize to dict for JSON storage'''
		return  { 'log_filename': self.log_filename
				, 'start_time': self.start_time.isoformat()
				, 'end_time': self.end_time.isoformat()
				}

class Task(object):
	def __init__(self, name, configuration, data={}):
		self.name = name
		self.script_path = os.path.join(configuration.base_dir, 'tasks', name, 'script.py')
		self.configuration = configuration

	def update_script(self, script):
		# Make sure folder exists first
		if not os.path.exists(os.path.dirname(self.script_path)):
			os.makedirs(os.path.dirname(self.script_path))
		with open(self.script_path, 'w') as fle:
			fle.write(script)

	@property
	def script(self):
		if self.script_path and os.path.exists(self.script_path):
			return open(self.script_path, 'r').read()
		return None

	def as_json(self):
		return dict()

	def run(self, log_file):
		process = subprocess.Popen(['python', self.script_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		log_file.write(process.communicate()[0])
		return process.returncode == 0
