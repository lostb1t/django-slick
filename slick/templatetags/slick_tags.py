import re
from collections import OrderedDict

from django import template
from django.contrib import admin

site = admin.site

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_app_list(context):
    request = context["request"]
    app_list = site.get_app_list(request)
    return app_list
