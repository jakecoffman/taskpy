import flask
import argparse
from flask.ext import admin

import taskpy.views
from taskpy.models.configuration import Configuration
from flask.ext.admin.contrib.sqlamodel import ModelView
from taskpy.models import db, Task, Job

def make_app():
	app = flask.Flask(__name__)
	app.secret_key = 'taskpy123'
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
	db.init_app(app)
	db.app = app
	db.create_all()

	index_view = taskpy.views.JobsView(name="Jobs", endpoint="jobs", url='/')
	admin_app = admin.Admin(app, name='Taskpy', index_view=index_view, base_template='admin_base.html')
	admin_app.add_view(taskpy.views.TasksView(name="Tasks", endpoint="tasks"))
	admin_app.add_view(ModelView(Task, db.session, name='Tasks', endpoint='tasks2'))
	admin_app.add_view(ModelView(Job, db.session, name='Jobs', endpoint='jobs2'))

	# Static bootstrap files (required by flask-admin)
	admin_app.add_view(taskpy.views.AdminStatic(url='/_'))

	configuration = Configuration('data')

	@app.before_request
	def before_request():
		flask.g.configuration = configuration

	return app

def main():
	# Setup argument parser
	parser = argparse.ArgumentParser()
	parser.add_argument("--host"
				, required=False, default='127.0.0.1'
				, help="Host interface to bind to")
	args = parser.parse_args()
	app = make_app()
	app.run(debug=True, host=args.host)

if __name__ == "__main__":
	main()
