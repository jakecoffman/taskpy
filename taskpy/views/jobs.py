import flask
import operator
from jinja2 import Markup
from flask.ext import admin, wtf
from flask.ext.admin.model import BaseModelView
import cgi

import taskpy.models.jobs

def format_status(context, model, field):
	'''Format status field to have an icon'''
	status = getattr(model, field)
	if not status:
		return Markup('<span class="label"><i class="icon-star-empty icon-white"></i> New</span>')
	elif status == "success":
		return Markup('<span class="label label-info"><i class="icon-thumbs-up icon-white"></i> Success</span>')
	else:
		return Markup('<span class="label label-important"><i class="icon-thumbs-down icon-white"></i> Failing</span>')

def format_name(context, model, field):
	'''Format job name as a link to the view page for that id'''
	url = flask.url_for('.job_view', id=getattr(model, field))
	return Markup('<a href="{url}">{field_value}</a>'.format(field_value=cgi.escape(getattr(model, field)), url=url))

class JobsForm(wtf.Form):
	'''Form for uploading an eventmap'''
	name = wtf.StringField(
		  validators = [wtf.DataRequired()]
		)

class JobsView(BaseModelView):
	column_formatters = dict(status=format_status, name=format_name)
	column_labels = dict(name='Job Name')
	column_sortable_list = ['name', 'status', 'last_run']

	list_template='jobs.html'

	def __init__(self, **options):
		super(JobsView, self).__init__(taskpy.models.jobs.Job, **options)

	def get_pk_value(self, model):
		return model.name

	def scaffold_list_columns(self):
		return ('name', 'status', 'last_run')

	def scaffold_form(self):
		return JobsForm

	def get_one(self, name):
		return flask.g.configuration.jobs.get(name)

	def get_list(self, page, sort_field, sort_desc, search, filters):
		lst = [obj for name, obj in flask.g.configuration.jobs.iteritems()]
		# Setting default sort
		if sort_field == None:
			sort_field='name'
			sort_desc=1

		lst.sort(key=operator.attrgetter(sort_field), reverse=bool(sort_desc))
		return len(lst), lst

	def create_model(self, form):
		name = form.name.data

		try:
			job = taskpy.models.jobs.Job(name=name)
			flask.g.configuration.add(job)
			flask.g.configuration.save()
			return True
		except Exception, ex:
			raise
			flask.flash('Failed create. {}: {}'.format(ex.__class__.__name__, str(ex)), category='error')
			return False

	def delete_model(self, model):
		try:
			flask.g.configuration.remove(model)
			flask.g.configuration.save()
			return True
		except Exception, ex:
			raise
			flask.flash('Failed create. {}: {}'.format(ex.__class__.__name__, str(ex)), category='error')
			return False

	@admin.expose('/job/<id>')
	def job_view(self, id):
		job = self.get_one(id)
		return self.render('job.html', job=job, job_old=flask.g.jobs.get(id), tasks=flask.g.tasks.get(), triggers=[])
