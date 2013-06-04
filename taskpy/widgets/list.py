from wtforms.fields.core import FieldList
from wtforms.widgets.core import ListWidget, HTMLString, html_params

class ExpandableListWidget(ListWidget):
	def __call__(self, field, **kwargs):
		kwargs.setdefault('id', field.id)
		html = ['<%s %s>' % (self.html_tag, html_params(**kwargs))]
		delete_btn = HTMLString('<a href="#" onclick="remove_task(this)" class="btn btn-danger"><i class="icon-trash"></i> Remove</a>')
		for subfield in field:
			html.append(
				'<li>%(field)s %(delete_btn)s</li>' %
					{ 'field': subfield()
					, 'delete_btn': delete_btn
					}
				)
		html.append('</%s>' % self.html_tag)
		lst = HTMLString(''.join(html))
		button = HTMLString('<input class="btn" type="button" onclick="new_task(); return true;" value="Add" />')
		return lst + button

class ExpandableFieldList(FieldList):
	widget = ExpandableListWidget()
