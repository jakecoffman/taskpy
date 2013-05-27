import os
import json
import iso8601
import datetime
import tempfile

class Job(object):
	def __init__(self, name, configuration, data={}):
		self.name = name
		self.tasks = [configuration.tasks.get(x) for x in data.get('tasks', [])]
		self.runs = [Run(self, x) for x in data.get('runs', [])]
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
			return self.runs[-1].state
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
		workspace = self.job.folder
		self.log_filename = log_file.name
		self.start_time = datetime.datetime.utcnow()
		self.state = 'running'
		status = True
		for task in self.job.tasks:
			log_file.write('Starting task "{0}" at {1}\n'.format(task.name, datetime.datetime.utcnow().isoformat()))
			status = task.run(log_file, workspace)
			if not status:
				break
		self.state = ('failed', 'success')[status]
		self.end_time = datetime.datetime.utcnow()
		log_file.write('Result: {0}\n'.format(self.state))
		log_file.write('Job ended at {0}\n'.format(self.end_time.isoformat()))
		self.job.configuration.save()

	def as_json(self):
		'''Serialize to dict for JSON storage'''
		return  { 'log_filename': self.log_filename
				, 'start_time': self.start_time.isoformat()
				, 'end_time': self.end_time.isoformat()
				, 'state': self.state
				}
	@property
	def output(self):
		if not os.path.exists(self.log_filename):
			return None
		return open(self.log_filename).read()

