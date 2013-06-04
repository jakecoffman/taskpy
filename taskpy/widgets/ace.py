import wtforms
from cgi import escape
from wtforms.widgets.core import HTMLString
from wtforms.compat import text_type
from wtforms import TextField

class AceEditorWidget(wtforms.widgets.TextArea):
	"""
	Renders an ACE code editor.
	"""
	def __call__(self, field, **kwargs): 
		kwargs.setdefault('id', field.id)
		html = '''
			<div id="{el_id}" style="height:500px;">{contents}</div>
			<textarea id="{el_id}_ace" name="{form_name}" style="display:none"></textarea>
			'''.format(
					  el_id=kwargs.get('id', field.id)
					, contents=escape(text_type(field._value()))
					, form_name=field.id
					)
		return HTMLString(html)

class AceEditorField(TextField):
    """
    An ACE code editor field to place in a wtforms form.
    """
    widget = AceEditorWidget()