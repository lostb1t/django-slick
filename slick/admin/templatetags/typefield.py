# -*- coding: utf-8 -*-
from django import template
from django.forms import DateTimeField
from django.forms.utils import ErrorList
register = template.Library()


@register.filter
def is_datetime(field):
    return isinstance(field.field, DateTimeField)


@register.filter
def field_type(field):
    return field.field.__class__.__name__


@register.filter
def get_type(value):
    return type(value)
