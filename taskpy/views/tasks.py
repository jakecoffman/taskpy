import cgi
import flask
import operator
from jinja2 import Markup
from flask.ext import admin, wtf
from flask.views import MethodView
from flask.ext.admin.model import BaseModelView
from taskpy.widgets.ace import AceEditorField

import taskpy.models.jobs

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
	def validate_name(self, field):
		if field.data in flask.g.configuration.tasks:
			raise wtf.ValidationError('That name already exists')

class TaskEditForm(TaskForm):
	def validate_name(self, field):
		# Dont allow duplicate names
		# Only validate when changing name!
		if field.data != flask.request.args.get('id'):
			if field.data in flask.g.configuration.tasks:
				raise wtf.ValidationError('That name already exists')

def format_name(view, context, model, field):
	'''Format job name as a link to the view page for that id'''
	url = flask.url_for('.edit_view', id=getattr(model, field))
	return Markup('<a href="{url}">{field_value}</a>'.format(field_value=cgi.escape(getattr(model, field)), url=url))

class TasksView(BaseModelView):
	column_formatters = dict(name=format_name)
	column_labels = dict(name='Task Name')
	column_sortable_list = ['name']

	edit_template = 'task.html'
	create_template = 'task.html'
	list_template = 'tasks.html'

	def __init__(self, **options):
		super(TasksView, self).__init__(taskpy.models.jobs.Task, **options)

	def scaffold_list_columns(self):
		return ('name',)

	def scaffold_form(self):
		return TaskForm

	def edit_form(self, obj):
		return TaskEditForm(obj=obj)

	def get_pk_value(self, model):
		return model.name

	def get_one(self, name):
		return flask.g.configuration.tasks.get(name)

	def get_list(self, page, sort_field, sort_desc, search, filters):
		lst = [obj for _, obj in flask.g.configuration.tasks.iteritems()]
		# Setting default sort
		if sort_field == None:
			sort_field='name'
			sort_desc=1

		lst.sort(key=operator.attrgetter(sort_field), reverse=bool(sort_desc))
		return len(lst), lst

	def create_model(self, form):
		model = taskpy.models.jobs.Task(name=form.name.data, configuration=flask.g.configuration)
		model.update_script(form.script.data)
		flask.g.configuration.add(model)
		flask.g.configuration.save()
		return True

	def delete_model(self, model):
		flask.g.configuration.remove(model)
		flask.g.configuration.save()

	def update_model(self, form, model):
		# Handle renaming
		if model.name != form.name.data:
			flask.g.configuration.remove(model)
			model.name = form.name.data
			flask.flash('Renamed to {}.'.format(model.name))

		# Handle other fields
		model.update_script(form.script.data)

		flask.g.configuration.add(model)
		flask.g.configuration.save()
		return True
