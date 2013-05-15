import flask
from flask.views import MethodView

import taskpy.models.tasks
import taskpy.models.jobs

class Task(MethodView):
    tasks = taskpy.models.tasks.TasksModel()
    jobs = taskpy.models.jobs.JobsModel()
    decorators = []

    # Get one task
    def get(self, task=None):
        if task not in self.tasks.get():
            flask.abort(404)
        included = []
        jobs = self.jobs.get()
        for job in jobs:
            if task in jobs[job]['Tasks']:
                included.append(job)
        included.sort()
        return flask.render_template('task.html', task=task, included=included, script=self.tasks.load_task(task))

    # Delete this task
    def delete(self, task=None):
        if task is None:
            flask.abort(405) # Not allowed
        return "Delete user", task

    # Update this task
    def put(self, task=None):
        print flask.request.mimetype
        if task is None:
            flask.abort(405) # Not allowed
        form = flask.request.form
        # This may be a rename operation if it's not in the list
        if form['name'] in self.tasks.get():
            self.tasks.save_task(form['name'], form['script'])
        else:
            raise NotImplementedError()
        return '/tasks/'
