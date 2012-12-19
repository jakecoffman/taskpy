import flask
import flask.views

from models import jobs, tasks

class Jobs(flask.views.MethodView):
    jobs = jobs.JobsModel()
    tasks = tasks.TasksModel()

    def get(self):
        return flask.render_template('jobs.html', jobs=self.jobs.get())

    def post(self):
        form = flask.request.form
        name = form['name']
        self.jobs.add_job(name)
        return '/jobs/'
