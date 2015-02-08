import re
from collections import OrderedDict

from django import template
from django.contrib.admin.helpers import AdminField
from django.core import serializers
from django.forms.models import model_to_dict
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

from ..widgets import FilteredSelectMultiple

site = admin.site

register = template.Library()


@register.tag
def capture(parser, token):
    nodelist = parser.parse(('endcapture',))
    parser.delete_first_token()
    varname = token.contents.split()[1]
    return CaptureNode(nodelist, varname)
 
class CaptureNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname
 
    def render(self, context):
        context[self.varname] = self.nodelist.render(context)
        return ''


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

    def render_tag(self, context, title, classes, tabs, **kwargs):

        nodelist = kwargs.pop('nodelist')
        body = nodelist.render(context)
        tabs_dict = None
        if tabs:
            tabs = tabs.split(",")
            tabs_dict = OrderedDict()
            for tab in tabs:
                k, v = tab.split(":")
                tabs_dict[k] = v

        context['panel_body'] = body
        context['panel_title'] = title
        context['panel_classes'] = classes
        context['panel_tabs'] = tabs_dict or None

        t = template.loader.get_template(self.template)
        c = template.Context(context)

        return t.render(c)

class SlickPanel(BasePanel):
    name = 'panel'
    template = 'slick/partials/panel.haml'
    options = Options(
        Argument('title', default=None, required=False),
        Argument('classes', default=None, required=False),
        Argument('tabs', default=None, required=False),
        blocks=[('endslickpanel', 'nodelist')],
    )

register.tag('slickpanel', SlickPanel)

class SlickTabs(Tag):
    name = 'panel'
    template = 'slick/partials/tab.haml'
    options = Options(
        MultiKeywordArgument('tabs', splitter=':', resolve=True),
    )
    def render_tag(self, context, tabs, **kwargs):
        #print tabs
        tabs_dict = OrderedDict()
        #print tabs
        if tabs:
            for k, v in tabs.items():
                #print {a.split("=")[0]: a.split("=")[1] for a in k.split(";")}
                attributes = {a.split("=")[0]: a.split("=")[1] for a in k.split(";")}
                attributes['id'] = attributes['title'].lower()
                attributes['content'] = v
                tabs_dict[attributes['id']] = attributes
                #for 
                #print attributes['title']
                #tabs_dict
        #print tabs_dict
        '''
              tabs_dict[]
            tabs = tabs.split(",")
            tabs_dict = OrderedDict()
            for tab in tabs:
                k, v = tab.split(":")
                tabs_dict[k] = v
        '''

        context['tabs'] = tabs_dict
        t = template.loader.get_template(self.template)
        c = template.Context(context)

        return t.render(c)

register.tag('slicktabs', SlickTabs)


class BlockTest(Tag):
    options = Options(
        Argument('name', resolve=False),
        blocks=[('sup', 'nodelist'), ('endblocktest', 'nodelist')],
    )

    def render_tag(self, context, **kwargs):
        pass

register.tag('blocktest', BlockTest)

'''
@register.inclusion_tag('slick/partials/tab.haml')
def SlickTab(*args, **kwargs):
    """
    Render a form
    """
    context = kwargs.copy()
    if args:
        tabs = OrderedDict()
        i = 0
        for tab in args:
            #print tab
            tabs[i] = tab
            i += 1
            #k, v = tab.split("
    #print tabs
    context['tabs'] = tabs
    return context
'''

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

# TODO Put in template suggestion for application.model
@register.simple_tag
def slick_render_action(action, *args, **kwargs): 
    #print action
    if action.action_object_object_id is not None and action.action_object is None:
        return ''

    if action.action_object is None:
        if action.verb.lower() in ['closed', 'reopened']:
            class_name = 'status'
        else:
            class_name = "action"
    else:
        class_name = action.action_object.__class__.__name__.lower()
    return render_to_string("slick/actions/%s.html" % class_name, {'action': action})


@register.assignment_tag
def slick_get_class_name(obj):
    return obj.__class__.__name__.lower()


@register.inclusion_tag('slick/partials/object_as_table.html', takes_context=True)
def slick_render_as_table(context, obj, **kwargs):
    #object_dict = model_to_dict(object)
    object_dict = serializers.serialize( "python", [obj,])

    #print object_dict[0]
    return {'object_dict': object_dict[0]}

'''
@register.filter
def slick_action_verbose_time(datetime):
    return datetime.timesince
'''
