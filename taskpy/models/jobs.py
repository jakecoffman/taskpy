import json
import os
import shutil
import time

import taskpy.models.tasks as task_list

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
        open('jobs.json', 'w').write(json.dumps(self._data))
    
    def load(self):
        if not os.path.isdir('data'):
            os.mkdir('data')
        if not os.path.isdir('data/jobs'):
            os.mkdir('data/jobs')
        if not os.path.isdir('data/tasks'):
            os.mkdir('data/tasks')
        try:
            self._data = json.loads(open('jobs.json').read())
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
        self._data[name] = {"Runs": []}
        self.save()
    
    # Wrap this function to update
    def update_job(self, form):
        name = form['name']
        if name not in self._data:
            raise Exception("Can't update job, it doesn't exist!")
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
        tasks = job['Tasks']
        folder = 'data/jobs/{0}/{1}'.format(name, run)
        if os.path.isdir(folder):
            # user clicked too fast
            return
        job['Runs'].append([run, 'running'])
        this_run = job['Runs'][-1]
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
        run = len(self._data[name]['Runs'])
        tasks = self._data[name]['Tasks']
        contents = []
        for task in tasks:
            contents.append(task_list.load_task(task))
        tasks = zip(tasks, contents)
        save_run(name, {'output':output, 'job':name, 'run':run, 'tasks':tasks})

    def save_run(self, name, js):
        job = self._data[name]
        run = job['Runs'][-1][0]
        folder = 'data/jobs/{0}/{1}'.format(name, run)
        f = open(folder + '/run.json', 'w')
        f.write(json.dumps(js))

    def get_page(self, name, run):
        run = int(run)
        job = self._data[name]
        if run < -1:
            runs = job['Runs']
            for i, r in enumerate(reversed(runs)):
                print i, r
                if r[1] == "success":
                    run = len(runs) - (i+1)
                    break
        elif run == -1:
            pass
        else:
            run -= 1
        run = job['Runs'][run][0]
        folder = 'data/jobs/{0}/{1}'.format(name, run)
        f = open(folder + '/run.html')
        return f.read()

    def get_run_args(self, job, run):
        run = self._data[job]['Runs'][int(run)-1][0]
        return json.loads(open('data/jobs/{0}/{1}/run.json'.format(job, run)).read())
