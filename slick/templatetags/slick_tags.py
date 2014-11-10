import re

from django import template
from django.contrib.admin.helpers import AdminField
from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.core.urlresolvers import reverse
from django.forms.widgets import TextInput, CheckboxInput, CheckboxSelectMultiple, RadioSelect
from django.contrib.admin import widgets
from django.template.loader import render_to_string

from classytags.arguments import Argument, MultiKeywordArgument, KeywordArgument
from classytags.core import Tag, Options
from classytags.helpers import InclusionTag

from ..settings import ADMIN_TITLE
from ..widgets import FilteredSelectMultiple

site = admin.site

register = template.Library()


@register.simple_tag()
def slick_admin_title():
    return ADMIN_TITLE


@register.assignment_tag(takes_context=True)
def is_active_path(context, name, by_path=False, on_subpath=False):
    """ Return the string 'active' current request.path is same as name
    
    Keyword aruguments:
    request  -- Django request object
    name     -- name of the url or the actual path
    by_path  -- True if name contains a url instead of url name
    on_subpath  -- True if active applies to items on the subpath
    """
    request = context["request"]

    if by_path:
        path = name
    else:
        path = reverse(name)

    if request.path == path or (on_subpath and request.path.startswith(path)):
        return True
 
    return False


@register.assignment_tag(takes_context=True)
def get_app_list(context):
    request = context["request"]
    app_dict = {}
    user = request.user
    for model, model_admin in site._registry.items():
        app_label = model._meta.app_label
        has_module_perms = user.has_module_perms(app_label)
        
        if has_module_perms:
            perms = model_admin.get_model_perms(request)
            
            if True in perms.values():
                model_dict = {
                    'name': capfirst(model._meta.verbose_name_plural),
                    'admin_url': mark_safe('/admin/%s/%s/' % (app_label, model.__name__.lower())),
                    'perms': perms,
                    'description': model_admin.description if hasattr(model_admin, 'description') else None
                }

                if app_label in app_dict:
                    app_dict[app_label]['models'].append(model_dict)
                else:
                    app_dict[app_label] = {
                        'name': app_label.title(),
                        'app_url': app_label + '/',
                        'admin_url': mark_safe('/admin/%s/' % (app_label)),
                        'has_module_perms': has_module_perms,
                        'models': [model_dict],
                    }
                    
    app_list = app_dict.values()
    app_list.sort(lambda x, y: cmp(x['name'], y['name']))
    return app_list



@register.filter
def slick_input_type(field):
    """
    Return input type to use for field
    """

    try:
        widget = field.field.widget
    except:
        raise ValueError("Expected a Field, got a %s" % type(field))

    if isinstance(widget, TextInput):
        return u'text'
    if isinstance(widget, CheckboxInput):
        return u'checkbox'
    if isinstance(widget, CheckboxSelectMultiple):
        return u'multicheckbox'
    if isinstance(widget, RadioSelect):
        return u'radioset'

    '''
    if isinstance(widget, widgets.RelatedFieldWidgetWrapper):
        #print widget.widget
        return u'select'
    '''
    
    return u'default'


class BasePanel(Tag):

    def render_tag(self, context, title, classes, collapse, **kwargs):

        nodelist = kwargs.pop('nodelist')
        body = nodelist.render(context)

        panel_context = self.get_panel_context(kwargs)
        panel_context['body'] = body
        panel_context['title'] = title.get('title', None)
        panel_context['classes'] = classes.get('classes', None)
        #print panel_context['collapse']
        panel_context['collapse'] = collapse.get('collapse', None)

        t = template.loader.get_template(self.template)
        c = template.Context(kwargs)

        return t.render(c)

    def get_panel_context(self, arguments):
        return arguments


class SlickPanel(BasePanel):
    name = 'panel'
    template = 'slick/panel.html'
    options = Options(
        KeywordArgument('title', required=False),
        KeywordArgument('classes', required=False),
        KeywordArgument('collapse', required=False),
        MultiKeywordArgument('kw', required=False),
        blocks=[('endslickpanel', 'nodelist')],
    )

    def get_panel_context(self, arguments):
        return arguments

register.tag('slickpanel', SlickPanel)


@register.inclusion_tag('slick/form.html')
def slick_form(form, **kwargs):
    """
    Render a form

    """
    context = kwargs.copy()
    context['form'] = form
    return context


@register.inclusion_tag('slick/field.html')
def slick_field(field, **kwargs):
    """
    Render a field

    kwargs:
        - show_label
    """
    context = kwargs.copy()
    
    if isinstance(field, AdminField):
        real_field = field.field
    else:
        real_field = field

    if isinstance(real_field.field.widget, widgets.RelatedFieldWidgetWrapper):
        # Replace FilteredSelectMultiple for related fields with our own
        if isinstance(real_field.field.widget.widget, widgets.FilteredSelectMultiple):
            widget = real_field.field.widget.widget
            real_field.field.widget.widget = FilteredSelectMultiple(verbose_name=widget.verbose_name, is_stacked=widget.is_stacked)

    context['field'] = real_field
    context['input_type'] = slick_input_type(real_field)
    return context


@register.filter(name='addattrs')
def addattrs(field, attributes):
    ''' render field. Allow adding attributes '''
    attrs = {}
    definition = attributes.split(',')
 
    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            t, v = d.split(':')
            attrs[t] = v

    if isinstance(field, AdminField):
        return field.field.as_widget(attrs=attrs)
    else:
        return field.as_widget(attrs=attrs)

"""
class RenderField(Tag):
     options = Options(
        MultiKeywordArgument('classes', required=False),
        MultiKeywordArgument('kwargs', required=False),
    )

    def render_tag(self, context, name, **kwargs):
        if isinstance(field, AdminField):
            return field.field.as_widget(attrs=attrs)
        else:
            return field.as_widget(attrs=attrs)

register.tag('render_field', RenderField)
"""

@register.filter(name='render_label')
def render_label(field, attributes):
    ''' render label. Allow adding attributes '''
    attrs = {}
    definition = attributes.split(',')
 
    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            t, v = d.split(':')
            attrs[t] = v

    return field.field.label_tag(attrs=attrs)


