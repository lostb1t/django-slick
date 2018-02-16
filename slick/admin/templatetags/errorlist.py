# -*- coding: utf-8 -*-
from django import template
from django.forms.utils import ErrorList
#from core.utils import SemanticErrorList

register = template.Library()

@register.filter
def as_pointing_label(errors):
    '''
    Generate top pointing label on semanti-ui format.

    Usage on template:
        {% load errorlist %}
        ...
        <label for="id_<your_field_name>">{% trans '<your_field_label>' %}</label>
        {{ form.<your_field_name> }}
        {{ form.<your_field_name>.errors|as_pointing_label }}
        ...
    '''
    if type(errors) is ErrorList:
        errors = errors.as_ul()

    if not errors:
        return u''

    errors = errors.replace(u'<ul class="errorlist">', '')
    errors = errors.replace(u'</ul>', '')
    errors = errors.replace(u'<li>', '')
    errors = errors.split(u'</li>')
    errors = [error for error in errors if error]
    result = SemanticErrorList(errors)
    return result.as_pointing_label()
