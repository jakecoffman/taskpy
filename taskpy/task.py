import flask

from taskpy.views.jobs import Jobs
from taskpy.views.job import Job
from taskpy.views.tasks import Tasks
from taskpy.views.task import Task
from taskpy.views.triggers import Triggers
from taskpy.views.trigger import Trigger


def make_app():
	app = flask.Flask(__name__)
	
	jobs = Jobs.as_view('jobs')
	app.add_url_rule("/", view_func=jobs)
	app.add_url_rule('/jobs', view_func=jobs)
	app.add_url_rule('/jobs/', view_func=jobs)

	job = Job.as_view('job')
	app.add_url_rule('/jobs/<job>', view_func=job)
	app.add_url_rule('/jobs/<job>/<run>', view_func=job)

	tasks = Tasks.as_view('tasks')
	app.add_url_rule('/tasks', view_func=tasks)
	app.add_url_rule('/tasks/', view_func=tasks)

	task = Task.as_view('task')
	app.add_url_rule('/tasks/<task>', view_func=task)

	triggers = Triggers.as_view('triggers')
	app.add_url_rule('/triggers', view_func=triggers)
	app.add_url_rule('/triggers/', view_func=triggers)

	trigger = Trigger.as_view('trigger')
	app.add_url_rule('/triggers/<trigger>', view_func=trigger)

	return app

def main():
	app = make_app()
	app.run(debug=True)

if __name__ == "__main__":
	main()
