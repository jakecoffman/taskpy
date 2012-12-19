import flask
import flask.views

from models import jobs, tasks

class Job(flask.views.MethodView):
    jobs = jobs.JobsModel()
    tasks = tasks.TasksModel()

    def get(self, job):
        if job not in self.jobs.get():
            flask.abort(404)
        return flask.render_template('job.html', name=job, job=self.jobs.get(job), tasks=self.tasks.get())

    def delete(self, job):
        return "Delete job", job

    def put(self, job):
        form = flask.request.form
        if form['name'] == job:
            tasks = form.getlist('task')
            triggers = form.getlist('trigger')
            self.jobs.update_job(form)
            self.jobs.save()
        # Renaming operation
        else:
            raise NotImplementedError()
        return '/jobs/'
