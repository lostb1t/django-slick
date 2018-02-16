from django import template
from django.core.urlresolvers import reverse_lazy

from ..utils import SideBar

register = template.Library()


@register.inclusion_tag('sidebar/sidebar.html')
def render_sidebar():
    sidebar = SideBar()
    return {
        'sidebar': sidebar,
    }
