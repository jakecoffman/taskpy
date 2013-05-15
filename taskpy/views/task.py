import flask
from flask.views import MethodView

class Task(MethodView):
    decorators = []

    # Get one task
    def get(self, task=None):
        if task not in flask.g.tasks.get():
            flask.abort(404)
        included = []
        jobs = flask.g.jobs.get()
        for job in jobs:
            if task in jobs[job].get('Tasks', []):
                included.append(job)
        included.sort()
        return flask.render_template('task.html', task=task, included=included, script=flask.g.tasks.load_task(task))

    # Delete this task
    def delete(self, task=None):
        if task is None:
            flask.abort(405) # Not allowed
        return "Delete user", task

    # Update this task
    def put(self, task=None):
        if task is None:
            flask.abort(405) # Not allowed
        form = flask.request.form
        # This may be a rename operation if it's not in the list
        if form['name'] in flask.g.tasks.get():
            flask.g.tasks.save_task(form['name'], form['script'])
        else:
            raise NotImplementedError()
        return '/tasks/'
