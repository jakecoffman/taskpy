import json
import os
import shutil
import time
import glob
import flask

import taskpy.models.tasks as task_list

class Configuration(object):
	def __init__(self, base_dir='data'):
		self.base_dir = base_dir
		self.jobs = {}
		self.load()

	def load(self):
		with open(os.path.join(self.base_dir, 'jobs.json'), 'r') as fle:
			jobs_data = json.load(fle)
		for name, data in jobs_data.iteritems():
			self.jobs[name] = Job( name=name
								 , data=data
								 , configuration=self
								 )

	def save(self):
		jobs_data = {job.name: job.as_json() for _, job in self.jobs.items()}
		with open(os.path.join(self.base_dir, 'jobs.json'), 'w') as fle:
			json.dump(jobs_data, fle)

	def add(self, obj):
		self.jobs[obj.name] = obj

	def remove(self, obj):
		self.jobs.pop(obj.name)

class Job(object):
	def __init__(self, name, data={}, configuration=None):
		self.name = name
		self.tasks = data.get('tasks', [])
		self.runs = data.get('runs', [])
		self.configuration = configuration

	def as_json(self):
		return  { 'name': self.name
				, 'tasks': self.tasks
				, 'runs': self.runs
				}

	@property
	def status(self):
		return None

	@property
	def last_run(self):
		return None

	@property
	def folder(self):
		return os.path.join(self.configuration.base_dir, 'jobs', self.name)

	def run(self):
		run_time = time.strftime('%Y%m%d%H%M%S')
		folder = os.path.join(self.folder, run_time)
		if os.path.isdir(folder):
			# user clicked too fast
			return
		this_run = [run_time, 'running']
		self.runs.append(this_run)
		self.configuration.save()
		os.makedirs(folder)
		log = open(os.path.join(folder, 'log.txt'), 'w')
		for task in self.tasks:
			log.write("Starting task: {0}\n".format(task))
			log.write("Task started at {0}\n".format(time.strftime('%d/%m/%Y %I:%M:%S %p')))
			ret = flask.g.tasks.run_task(task, log)
			log.write("Task ended at {0}\n".format(time.strftime('%d/%m/%Y %I:%M:%S %p')))
			if ret != 0:
				this_run[1] = 'fail'
				log.write("Task failed, quitting")
				break
		if this_run[1] == 'running':
			this_run[1] = 'success'
		log.write("Job completed successfully")
		self.configuration.save()
		log.close()

class JobsModel(object):
    def __init__(self):
        self._data = dict()
        self.load()

    # Returns all of the jobs or returns a job if provided
    def get(self, job=None):
        if job is None:
            return self._data
        if job in self._data:
            return self._data[job]
        else:
            return None

    def save(self):
        open('data/jobs.json', 'w').write(json.dumps(self._data))
    
    def load(self):
        if not os.path.isdir('data'):
            os.mkdir('data')
        if not os.path.isdir('data/jobs'):
            os.mkdir('data/jobs')
        if not os.path.isdir('data/tasks'):
            os.mkdir('data/tasks')
        try:
            self._data = json.loads(open('data/jobs.json').read())
        except:
            self._data = dict()
            self.save()
    
    def add_job(self, name):
        if name in self._data:
            raise Exception("Error: Job name already exists.")
        folder = "data/jobs/{0}".format(name)
        if os.path.isdir(folder):
            os.remove(folder)
        os.mkdir(folder)
        self._data[name] = {"runs": []}
        self.save()
    
    # Wrap this function to update
    def update_job(self, form):
        name = form.get('name')
        job = self._data.get(name)
        if not job:
            raise Exception("Can't update job, it doesn't exist!")
        if 'task' in form:
            job['tasks'] = form.getlist('task')
        return name
    
    def delete_job(self, job):
        if job not in self._data:
            raise Exception("Error: Job doesn't exist")
        try:
            shutil.rmtree('data/jobs/{0}'.format(job))
        except Exception as e:
            #todo: log
            print e
        del self._data[job]
        self.save()

    def run_job(self, name):
        job = self._data[name]
        run = time.strftime('%Y%m%d%H%M%S')
        tasks = job['tasks']
        folder = 'data/jobs/{0}/{1}'.format(name, run)
        if os.path.isdir(folder):
            # user clicked too fast
            return
        job['runs'].append([run, 'running'])
        this_run = job['runs'][-1]
        self.save()
        os.mkdir(folder)
        log = open(folder+'/log.txt', 'w')
        for task in tasks:
            log.write("Starting task: {0}\n".format(task))
            log.write("Task started at {0}\n".format(time.strftime('%d/%m/%Y %I:%M:%S %p')))
            ret = task_list.run_task(task, log)
            log.write("Task ended at {0}\n".format(time.strftime('%d/%m/%Y %I:%M:%S %p')))
            if ret != 0:
                this_run[1] = 'fail'
                log.write("Task failed, quitting")
                break
        if this_run[1] == 'running':
            this_run[1] = 'success'
            log.write("Job completed successfully")
        self.save()
        log.close()
        output = open(folder+'/log.txt').read()
        # Render the template to freeze it in time
        run = len(self._data[name]['runs'])
        tasks = self._data[name]['tasks']
        contents = []
        for task in tasks:
            contents.append(task_list.load_task(task))
        tasks = zip(tasks, contents)
        save_run(name, {'output':output, 'job':name, 'run':run, 'tasks':tasks})

    def save_run(self, name, js):
        job = self._data[name]
        run = job['runs'][-1][0]
        folder = 'data/jobs/{0}/{1}'.format(name, run)
        f = open(folder + '/run.json', 'w')
        f.write(json.dumps(js))

    def get_page(self, name, run):
        run = int(run)
        job = self._data[name]
        if run < -1:
            runs = job['runs']
            for i, r in enumerate(reversed(runs)):
                print i, r
                if r[1] == "success":
                    run = len(runs) - (i+1)
                    break
        elif run == -1:
            pass
        else:
            run -= 1
        run = job['runs'][run][0]
        folder = 'data/jobs/{0}/{1}'.format(name, run)
        f = open(folder + '/run.html')
        return f.read()

    def get_run_args(self, job, run):
        run = self._data[job]['runs'][int(run)-1][0]
        return json.loads(open('data/jobs/{0}/{1}/run.json'.format(job, run)).read())
