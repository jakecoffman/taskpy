import os
import subprocess

class TasksModel(object):
    def __init__(self):
        self._data = list()
        self.load()

    def get(self):
        return self._data

    def load(self):
        self._data = list()
        if not os.path.isdir('data/tasks'):
            os.mkdir('data/tasks')
        tasks = os.listdir('data/tasks')
        for task in tasks:
            if task.endswith('.py'):
                self._data.append(task.split('.')[0])

    def save_task(self, name, script):
        open("data/tasks/{0}.py".format(name), 'w').write(script)
        if name not in self._data:
            self._data.append(name)

    def load_task(self, name):
        f = "data/tasks/{0}.py".format(name)
        if os.path.isfile(f):
            return open("data/tasks/{0}.py".format(name), 'r').read()
        else:
            return None
    
    def delete_task(self, name):
        if name in self._data:
            os.remove("data/tasks/{0}.py".format(name))
            self.remove(name)
        else:
            raise Exception("Can't delete: task does not exist")
    
    # Todo, make thread pool run this
    def run_task(self, script, log):
        p = subprocess.Popen('python "data/tasks/{0}.py"'.format(script), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log.write(p.communicate()[0])
        return p.returncode
    