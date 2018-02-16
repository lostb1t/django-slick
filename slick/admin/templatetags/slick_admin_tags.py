import re

from django import template

register = template.Library()


@register.filter
def get_selected_choice(choices):
    for choice in choices:
        print choice
        if choice.selected:
            return choice
    return None
