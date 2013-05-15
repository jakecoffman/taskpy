import flask
from flask.views import MethodView

class Tasks(MethodView):

    # Get list of tasks, or get one task
    def get(self):
        return flask.render_template('tasks.html', tasks=flask.g.tasks.get())

    # Add new task
    def post(self):
        form = flask.request.form
        name = form['name']
        script = ''
        if 'script' in form:
            script = form['script']
        flask.g.tasks.save_task(name, script)
        return '/tasks/'
