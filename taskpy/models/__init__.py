import os
import stat
import tempfile
from flask import current_app as app
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Job(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=True, nullable=False, index=True)

	tasks = db.relationship('Task', secondary='job_tasks', lazy='joined')
	runs = db.relationship('Run')

	@property
	def status(self):
		if len(self.runs) != 0:
			return self.runs[-1].result

	def __unicode__(self):
		return self.name

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=True, nullable=False, index=True)
	script_path = db.Column(db.String(120))

	@property
	def script(self):
		if self.script_path and os.path.exists(self.script_path):
			return open(self.script_path, 'rU').read()
		return None

	@script.setter
	def script(self, value):
		self.script_path = os.path.join(app.config['TASKPY_BASE'], 'tasks', self.name, 'script')
		# Make sure folder exists first
		if not os.path.exists(os.path.dirname(self.script_path)):
			os.makedirs(os.path.dirname(self.script_path))
		# Make sure folder exists first
		with open(self.script_path, 'w') as fle:
			# Write to file, but use native line sep!
			for line in value.split('\n'):
				fle.write(line.rstrip())
				fle.write(os.linesep)
		os.chmod(self.script_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

	def __unicode__(self):
		return self.name

	def as_json(self):
		return {
			  'id': self.id
			, 'name': self.name
			, 'script': self.script
			}

class JobTasks(db.Model):
	__tablename__ = 'job_tasks'
	id = db.Column(db.Integer, primary_key=True)
	job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
	task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
	order = db.Column(db.Integer)

class Run(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
	start_time = db.Column(db.DateTime, nullable=False)
	end_time = db.Column(db.DateTime)
	result = db.Column(db.Enum('success', 'failed'))
	celery_id = db.Column(db.String(255), nullable=False)

	tasks = db.relationship('TaskResult')

class TaskResult(db.Model):
	__tablename__ = 'task_result'
	id = db.Column(db.Integer, primary_key=True)
	run_id = db.Column(db.Integer, db.ForeignKey('run.id'), nullable=False)
	parent_id = db.Column(db.Integer, db.ForeignKey('task_result.id'))
	task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
	log_file = db.Column(db.String(255))
	return_code = db.Column(db.Integer)
	start_time = db.Column(db.DateTime, nullable=False)
	end_time = db.Column(db.DateTime)

	task = db.relationship('Task')

	@property
	def output(self):
		if self.log_file and os.path.exists(self.log_file):
			return open(self.log_file, 'rU').read()
		return None
