import flask

import taskpy.views
import taskpy.models.jobs
import taskpy.models.tasks

def make_app():
	app = flask.Flask(__name__)
	
	jobs = taskpy.views.Jobs.as_view('jobs')
	app.add_url_rule("/", view_func=jobs)
	app.add_url_rule('/jobs', view_func=jobs)
	app.add_url_rule('/jobs/', view_func=jobs)

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

	@app.before_request
	def before_request():
		flask.g.jobs = jobs_model
		flask.g.tasks = tasks_model

	return app

def main():
	app = make_app()
	app.run(debug=True)

if __name__ == "__main__":
	main()
