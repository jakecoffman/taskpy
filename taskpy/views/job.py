import flask
import flask.views

class Job(flask.views.MethodView):

    def get(self, job):
        if job not in flask.g.jobs.get():
            flask.abort(404)
        return flask.render_template('job.html', name=job, job=flask.g.jobs.get(job), tasks=flask.g.tasks.get(), triggers=[])

    def delete(self, job):
        return "Delete job", job

    def post(self, job):
        form = flask.request.form
        if form['name'] == job:
            flask.g.jobs.update_job(form)
            flask.g.jobs.save()
        # Renaming operation
        else:
            raise NotImplementedError()
        return flask.redirect('/jobs/{}'.format(job))
