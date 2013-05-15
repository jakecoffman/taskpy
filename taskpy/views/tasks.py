import flask
from flask.views import MethodView

import taskpy.models.tasks
import taskpy.models.jobs

class Tasks(MethodView):
    tasks = taskpy.models.tasks.TasksModel()
    jobs = taskpy.models.jobs.JobsModel()
    decorators = []

    # Get list of tasks, or get one task
    def get(self):
        return flask.render_template('tasks.html', tasks=self.tasks.get())

    # Add new task
    def post(self):
        form = flask.request.form
        name = form['name']
        script = ''
        if 'script' in form:
            script = form['script']
        self.tasks.save_task(name, script)
        return '/tasks/'
