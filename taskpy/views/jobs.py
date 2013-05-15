import flask
import flask.views

class Jobs(flask.views.MethodView):
    def get(self):
        return flask.render_template('jobs.html', jobs=flask.g.jobs.get())

    def post(self):
        form = flask.request.form
        name = form['name']
        flask.g.jobs.add_job(name)
        return '/jobs/'
