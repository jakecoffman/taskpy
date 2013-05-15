import flask
import flask.views

class Job(flask.views.MethodView):

    def get(self, job):
        if job not in flask.g.jobs.get():
            flask.abort(404)
        return flask.render_template('job.html', name=job, job=flask.g.jobs.get(job), tasks=flask.g.tasks.get())

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
