import flask
taskpy = flask.Flask(__name__)

from views.jobs import Jobs
from views.job import Job
from views.tasks import Tasks
from views.task import Task
from views.triggers import Triggers
from views.trigger import Trigger

jobs = Jobs.as_view('jobs')
taskpy.add_url_rule("/", view_func=jobs)
taskpy.add_url_rule('/jobs', view_func=jobs)
taskpy.add_url_rule('/jobs/', view_func=jobs)

job = Job.as_view('job')
taskpy.add_url_rule('/jobs/<job>', view_func=job)
taskpy.add_url_rule('/jobs/<job>/<run>', view_func=job)

tasks = Tasks.as_view('tasks')
taskpy.add_url_rule('/tasks', view_func=tasks)
taskpy.add_url_rule('/tasks/', view_func=tasks)

task = Task.as_view('task')
taskpy.add_url_rule('/tasks/<task>', view_func=task)

triggers = Triggers.as_view('triggers')
taskpy.add_url_rule('/triggers', view_func=triggers)
taskpy.add_url_rule('/triggers/', view_func=triggers)

trigger = Trigger.as_view('trigger')
taskpy.add_url_rule('/triggers/<trigger>', view_func=trigger)

if __name__ == "__main__":

    taskpy.debug = True

    taskpy.run()
