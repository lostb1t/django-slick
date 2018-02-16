# -*- coding: utf-8 -*-
from django import template
from django.utils.html import escapejs, format_html
from django.utils.safestring import mark_safe
from django.contrib.admin.views.main import (
    ALL_VAR, ORDER_VAR, PAGE_VAR, SEARCH_VAR,
)

register = template.Library()

DOT = '.'
FIRST_ICON = 'angle double left'
PREVIOUS_ICON = 'angle left'
NEXT_ICON = 'angle right'
LAST_ICON = 'angle double right'
DISABLED_ICON_ITEM = '<div class="disabled item"><i class="{} icon"></i></div>'
LINK_ICON_ITEM = '<a href="{}" class="item"><i class="{} icon"></i></a>'
DOTS_ITEM = '<div class="disabled item">...</div>'
ACTIVE_ITEM = '<div class="item active">{}</div>'
LINK_ITEM = '<a href="{}" class="item">{}</a> '


'''
  Usage:
    - in pagination.html template:
    {% load paginator %}
    
    ...
    
    {% first_link cl %}
    {% previous_link cl %}
    
    {% if pagination_required %}
        {% for i in page_range %}
            {% paginator_number cl i %}
        {% endfor %}
    {% endif %}

    {% next_link cl %}
    {% last_link cl %}
    
    ...
'''


def paginator_link(cl, criteria, icon, page):
    '''
    Generates html for a disabled item or a link item
    '''
    if cl.page_num == criteria:
        return format_html(DISABLED_ICON_ITEM, mark_safe(icon))
    else:
        return format_html(LINK_ICON_ITEM, 
                           cl.get_query_string({PAGE_VAR: page}), 
                           mark_safe(icon))


@register.simple_tag
def first_link(cl):
    '''
    Defines link with icon to first page
    '''
    criteria = 0
    icon = FIRST_ICON
    page = 0
    return paginator_link(cl, criteria, icon, page)


@register.simple_tag
def previous_link(cl):
    '''
    Defines link with icon to previous page
    '''
    criteria = 0
    icon = PREVIOUS_ICON
    page = cl.page_num - 1
    return paginator_link(cl, criteria, icon, page)


@register.simple_tag
def next_link(cl):
    '''
    Defines link with icon to next page
    '''
    criteria = cl.paginator.num_pages - 1
    icon = NEXT_ICON
    page = cl.page_num + 1
    return paginator_link(cl, criteria, icon, page)


@register.simple_tag
def last_link(cl):
    '''
    Defines link with icon to last page
    '''
    criteria = cl.paginator.num_pages - 1
    icon = LAST_ICON
    page = cl.paginator.num_pages - 1
    return paginator_link(cl, criteria, icon, page)


@register.simple_tag
def paginator_number(cl, i):
    """
    Generates an individual page index link in a paginated list.
    """
    if i == DOT:
        return format_html(DOTS_ITEM)
    elif i == cl.page_num:
        return format_html(ACTIVE_ITEM, i + 1)
    else:
        return format_html(LINK_ITEM,
                           cl.get_query_string({PAGE_VAR: i}),
                           i + 1)
