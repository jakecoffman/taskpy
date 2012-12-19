import flask
from flask.views import MethodView

import models.triggers as trigger_list

class Trigger(MethodView):
    # Get one trigger
    def get(self, trigger):
        trigger_list.load()
        return flask.render_template('trigger.html', trigger=trigger_list.get()[trigger])

    # Delete a trigger
    def delete(self, trigger):
        return "Delete user", trigger

    # Update trigger
    def put(self, trigger):
        form = flask.request.form
        # This may be a rename operation if it's not in the list
        if form['name'] in trigger_list.get():
            trigger_list.save_trigger(form['name'], form['script'])
        else:
            raise NotImplementedError()
        return '/triggers/'
