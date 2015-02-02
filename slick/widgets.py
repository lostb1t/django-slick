from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.forms.widgets import Input
from django.core.exceptions import ImproperlyConfigured
from django.utils.html import conditional_escape, format_html


class FilteredSelectMultiple(forms.SelectMultiple):
    def __init__(self, verbose_name, is_stacked, attrs=None, choices=()):
        self.verbose_name = verbose_name
        self.is_stacked = is_stacked
        super(FilteredSelectMultiple, self).__init__(attrs, choices)

    def render(self, name, value, attrs=None, choices=()):
        if attrs is None:
            attrs = {}
        
        if self.is_stacked:
            attrs['class'] += 'stacked'

        attrs['data-selected-text-format'] = 'count'
        attrs['data-live-search'] = True
        attrs['class'] += ' selectpicker'
        output = [super(FilteredSelectMultiple, self).render(name, value, attrs, choices)]

        '''
        output.append('<script type="text/javascript">addEvent(window, "load", function(e) {')
        # TODO: "id_" is hard-coded here. This should instead use the correct
        # API to determine the ID dynamically.
        output.append('SelectFilter.init("id_%s", "%s", %s, "%s"); });</script>\n'
            % (name, self.verbose_name.replace('"', '\\"'), int(self.is_stacked), static('admin/')))
        '''
        return mark_safe(''.join(output))


class CheckboxChoiceInput(forms.widgets.CheckboxChoiceInput):
    input_type = 'checkbox'

    def render(self, name=None, value=None, attrs=None, choices=()):
        if self.id_for_label:
            label_for = format_html(' for="{0}"', self.id_for_label)
        else:
            label_for = ''
        html = format_html('{1}<label{0}> {2}</label>', label_for, self.tag(), self.choice_label)
        return html


class CheckboxFieldRenderer(forms.widgets.ChoiceFieldRenderer):
    choice_input_class = CheckboxChoiceInput
    def render(self):
        """
        Outputs a <ul> for this set of choice fields.
        If an id was given to the field, it is applied to the <ul> (each
        item in the list will get an id of `$id_$i`).
        """
        id_ = self.attrs.get('id', None)
        start_tag = format_html('<ul id="{0}">', id_) if id_ else '<ul>'
        output = [start_tag]
        for i, choice in enumerate(self.choices):
            choice_value, choice_label = choice
            if isinstance(choice_label, (tuple, list)):
                attrs_plus = self.attrs.copy()
                if id_:
                    attrs_plus['id'] += '_{0}'.format(i)
                sub_ul_renderer = ChoiceFieldRenderer(name=self.name,
                                                      value=self.value,
                                                      attrs=attrs_plus,
                                                      choices=choice_label)
                sub_ul_renderer.choice_input_class = self.choice_input_class
                output.append(format_html('<li>{0}{1}</li>', choice_value,
                                          sub_ul_renderer.render()))
            else:
                w = self.choice_input_class(self.name, self.value,
                                            self.attrs.copy(), choice, i)
                output.append(format_html('<li>{0}</li>', mark_safe(w)))
        output.append('</ul>')
        return mark_safe('\n'.join(output))


class PrettyCheckboxSelectMultiple(forms.widgets.CheckboxSelectMultiple):
    renderer = CheckboxFieldRenderer
    _empty_value = []

