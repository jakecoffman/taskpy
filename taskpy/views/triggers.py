import flask
from flask.views import MethodView

import taskpy.models.triggers as trigger_list

class Triggers(MethodView):
    # Get a list of triggers, or one trigger
    def get(self, trigger=None):
        trigger_list.load()
        # /triggers/
        return flask.render_template('triggers.html', triggers=trigger_list.get())

    # Add new trigger to triggers
    def post(self, trigger=None):
        form = flask.request.form
        name = form['name']
        script = ''
        if 'script' in form:
            script = form['script']
        trigger_list.add_trigger(name)
        return '/triggers/'
