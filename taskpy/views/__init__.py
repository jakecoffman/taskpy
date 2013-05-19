from taskpy.views.jobs import JobsView
from taskpy.views.tasks import TasksView
from taskpy.views.task import Task
from taskpy.views.triggers import Triggers
from taskpy.views.trigger import Trigger
from flask.ext import admin

__author__ = 'jake'

class AdminStatic(admin.AdminIndexView):
	def is_accessible(self):
		return False