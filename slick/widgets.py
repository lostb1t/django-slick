from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text


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