from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Job(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=True, nullable=False, index=True)

	tasks = db.relationship('Task', secondary='job_tasks', lazy='joined')

	def __unicode__(self):
		return self.name

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=True, nullable=False, index=True)

	def __unicode__(self):
		return self.name

class JobTasks(db.Model):
	__tablename__ = 'job_tasks'
	id = db.Column(db.Integer, primary_key=True)
	job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
	task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
