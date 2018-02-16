# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter
def help_text_as_placeholder(field):
    '''
    Usage: 
      {% load help_text_as_placeholder %}
      form.field|help_text_as_placeholder
      OR
      field|help_text_as_placeholder
    '''
    placeholder = unicode(field.help_text) or unicode(field.label)
    attrs = field.field.widget.attrs
    attrs.update({u'placeholder': placeholder})
    field.field.widget.attrs = attrs
    return field
