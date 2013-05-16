import flask
from flask.ext import admin

import taskpy.views
import taskpy.models.jobs
import taskpy.models.tasks

def make_app():
	app = flask.Flask(__name__)
	app.secret_key = 'taskpy123'
	
	index_view = taskpy.views.JobsView(name="Jobs", endpoint="jobs", url='/')
	admin_app = admin.Admin(app, name='Taskpy', index_view=index_view, base_template='admin_base.html')

	# Static bootstrap files (required by flask-admin)
	admin_app.add_view(taskpy.views.AdminStatic(url='/_'))

	job = taskpy.views.Job.as_view('job')
	app.add_url_rule('/jobs/<job>', view_func=job)
	app.add_url_rule('/jobs/<job>/<run>', view_func=job)

	tasks = taskpy.views.Tasks.as_view('tasks')
	app.add_url_rule('/tasks', view_func=tasks)
	app.add_url_rule('/tasks/', view_func=tasks)

	task = taskpy.views.Task.as_view('task')
	app.add_url_rule('/tasks/<task>', view_func=task)

	triggers = taskpy.views.Triggers.as_view('triggers')
	app.add_url_rule('/triggers', view_func=triggers)
	app.add_url_rule('/triggers/', view_func=triggers)

	trigger = taskpy.views.Trigger.as_view('trigger')
	app.add_url_rule('/triggers/<trigger>', view_func=trigger)

	jobs_model = taskpy.models.jobs.JobsModel()
	tasks_model = taskpy.models.tasks.TasksModel()
	configuration = taskpy.models.jobs.Configuration('.')

	@app.before_request
	def before_request():
		flask.g.jobs = jobs_model
		flask.g.tasks = tasks_model
		flask.g.configuration = configuration

	return app

def main():
	app = make_app()
	app.run(debug=True, host='0.0.0.0')

if __name__ == "__main__":
	main()
