import flask
from jinja2 import Markup
from flask.ext import admin, wtf
from flask.ext.admin.contrib.sqlamodel import ModelView
from taskpy.widgets.ace import AceEditorField

import taskpy.models

class TaskForm(wtf.Form):
	'''Form for creating a new job'''
	name = wtf.StringField(
		  validators = [wtf.DataRequired(), wtf.Regexp('^[a-zA-Z0-9_\-]*$')]
		)
	script = AceEditorField(
		  validators = [wtf.DataRequired()]
		, default='''#!/usr/bin/env python

def main():
	print 'Hello world!'

if __name__ == '__main__':
	main()
'''
		)

def format_name(view, context, model, field):
	'''Format job name as a link to the view page for that id'''
	url = flask.url_for('.edit_view', id=model.id)
	return Markup('<a href="{url}">%s</a>'.format(url=url)) % getattr(model, field)

class TasksView(ModelView):
	column_formatters = dict(name=format_name)
	column_labels = dict(name='Task Name')

	edit_template = 'task.html'
	create_template = 'task.html'
	list_template = 'tasks.html'

	def __init__(self, **options):
		super(TasksView, self).__init__(taskpy.models.Task, taskpy.models.db.session, **options)

	def scaffold_list_columns(self):
		return ('name',)

	def scaffold_form(self):
		return TaskForm
