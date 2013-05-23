import os
import json

from taskpy.models.jobs import Job
from taskpy.models.tasks import Task

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