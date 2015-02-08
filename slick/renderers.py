from django.forms import (
    TextInput, DateInput, FileInput, CheckboxInput,
    ClearableFileInput, Select, RadioSelect, CheckboxSelectMultiple, SelectMultiple
)
from django.forms.extras import SelectDateWidget
from django.utils.html import conditional_escape, strip_tags

from bootstrap3.renderers import FieldRenderer as BaseFieldRenderer
from bootstrap3.forms import (render_form, render_field, render_label, render_form_group,
                    is_widget_with_placeholder, is_widget_required_attribute, FORM_GROUP_CLASS)


from .widgets import PrettyCheckboxSelectMultiple


class FieldRenderer(BaseFieldRenderer):
    def __init__(self, field, *args, **kwargs):
        super(FieldRenderer, self).__init__(field, *args, **kwargs)
        
        #print self.widget
        #if isinstance(self.widget, CheckboxSelectMultiple):
        if isinstance(self.widget, (CheckboxSelectMultiple, SelectMultiple)):   # hehehe
            widget = self.widget
            self.widget = PrettyCheckboxSelectMultiple()
            self.widget.attrs = self.initial_attrs
            self.widget.choices = widget.choices
            self.field.field.widget = self.widget

    def post_widget_render(self, html):
        if isinstance(self.widget, RadioSelect):
            html = self.list_to_class(html, 'radio')
        elif isinstance(self.widget, CheckboxSelectMultiple):
            html = self.list_to_class(html, 'checkbox')
        elif isinstance(self.widget, SelectDateWidget):
            html = self.fix_date_select_input(html)
        elif isinstance(self.widget, ClearableFileInput):
            html = self.fix_clearable_file_input(html)
        elif isinstance(self.widget, CheckboxInput):
            label = render_label(content=self.field.label, label_for=self.field.id_for_label, label_title=strip_tags(self.field_help))
            html = "%s %s" % (html, label)

        return html