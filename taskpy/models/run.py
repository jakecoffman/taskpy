import datetime
import iso8601

def load_time(data, field):
	'''Unserialize the string formatted time into datetime.datetime'''
	if field in data:
		return iso8601.parse_date(data.get(field))
	return None

class RunConfig(object):
	def __init__(self, job):
		self.tasks = [task.as_json() for task in job.tasks]

class RunResult(object):
	def __init__(self, data={}, celery_id=None):
		self.state = data.get('state')
		self.start_time = load_time(data, 'start_time')
		self.end_time = load_time(data, 'end_time')
		self.celery_id = data.get('celery_id', celery_id)
		# If data['celery_id'] was None, use the param.
		if self.celery_id == None:
			self.celery_id = celery_id
		self.tasks = []
		for task in data.get('tasks', []):
			task['end_time'] = load_time(task, 'end_time')
			self.tasks.append(task)
	def record_begin(self):
		self.start_time = datetime.datetime.utcnow()
		self.state = 'running'
	def record_task(self, task_id, output, return_code):
		self.tasks.append({
			  'task_id': task_id
			, 'output': output
			, 'return_code': return_code
			, 'end_time': datetime.datetime.utcnow()
			})
	def record_end(self, success):
		self.end_time = datetime.datetime.utcnow()
		self.state = ('failed', 'success')[success]
	def as_json(self):
		tasks = []
		for task in self.tasks:
			r = {key: val for key, val in task.iteritems() if not isinstance(val, datetime.datetime)}
			r.update({key: val.isoformat() for key, val in task.iteritems() if isinstance(val, datetime.datetime)})
			tasks.append(r)
		return {
			  'state': self.state
			, 'start_time': self.start_time.isoformat()
			, 'end_time': self.end_time.isoformat()
			, 'celery_id': self.celery_id
			, 'tasks': tasks
			}