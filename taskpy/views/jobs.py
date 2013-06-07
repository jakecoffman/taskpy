import cgi
import flask
from jinja2 import Markup
from flask.ext import admin, wtf
from flask.ext.admin.contrib.sqlamodel import ModelView
from wtforms.ext.sqlalchemy.fields import QuerySelectField

import taskpy.models
from taskpy.widgets.list import ExpandableFieldList

def format_status(view, context, model, field):
	'''Format status field to have an icon'''
	status = getattr(model, field)
	if not status:
		return Markup('<span class="label"><i class="icon-star-empty icon-white"></i> New</span>')
	elif status == "success":
		return Markup('<span class="label label-success"><i class="icon-thumbs-up icon-white"></i> Success</span>')
	else:
		return Markup('<span class="label label-important"><i class="icon-thumbs-down icon-white"></i> Failing</span>')

def format_name(view, context, model, field):
	'''Format job name as a link to the view page for that id'''
	url = flask.url_for('.job_view', id=model.id)
	return Markup('<a href="{url}">{field_value}</a>'.format(field_value=cgi.escape(getattr(model, field)), url=url))

def format_count(view, context, model, field):
	'''Format the task count in a badge'''
	return Markup('<div class="badge badge-inverse">%(field_value)s</div>') % {'field_value': len(getattr(model, field))}

class JobForm(wtf.Form):
	'''Form for editing a job'''
	name = wtf.StringField(
		  validators = [wtf.DataRequired(), wtf.Regexp('^[a-zA-Z0-9_\-]*$')]
		)
	tasks = ExpandableFieldList(
		  QuerySelectField(
			  'Task'
			, query_factory=lambda: taskpy.models.Task.query
			, validators=[wtf.InputRequired()]
			, get_label=lambda x: x.name
			)
		, min_entries=1
		)

class JobsView(ModelView):
	column_formatters = dict(status=format_status, name=format_name, tasks=format_count)
	column_labels = dict(name='Job Name')

	list_template='jobs.html'
	edit_template='job_edit.html'
	create_template='job_edit.html'

	def __init__(self, **options):
		super(JobsView, self).__init__(taskpy.models.Job, taskpy.models.db.session, **options)

	def get_pk_value(self, model):
		return model.name

	def scaffold_list_columns(self):
		return ('name', 'tasks', 'status', 'last_run')

	def scaffold_form(self):
		return JobForm

	@admin.expose('/job/<id>')
	def job_view(self, id):
		job = self.get_one(id)
		if not job:
			return flask.redirect(flask.url_for('.index_view'))
		here = flask.url_for('.job_view', id=id)
		return self.render('job.html', job=job, return_url=here)

	@admin.expose('/job/<id>/run')
	def start_run_view(self, id):
		job = self.get_one(id)
		if not job:
			return flask.redirect(flask.url_for('.index_view'))
		job.run()
		return flask.redirect(flask.url_for('.job_view', id=id))

	@admin.expose('/job/<id>/runs/<run_id>')
	def run_view(self, id, run_id):
		job = self.get_one(id)
		if not job:
			return flask.redirect(flask.url_for('.job_view', id=id))
		run = job.get_run(run_id)
		if not run:
			return flask.redirect(flask.url_for('.job_view', id=id))
		here = flask.url_for('.run_view', id=id, run_id=run_id)
		return self.render('run.html', run=run, job=job, return_url=here)
