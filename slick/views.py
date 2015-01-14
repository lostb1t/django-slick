import json

from django.http import HttpResponse
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
#from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.views.generic.base import ContextMixin
from django.views.generic import TemplateView
from django.utils.encoding import force_text
from django.contrib.contenttypes.models import ContentType
from django.forms.models import model_to_dict
from django.db.models import get_model, get_models, get_app
from django.views.generic import View
from django.contrib.admin.util import (lookup_field, display_for_field, display_for_value, label_for_field)

from djangular.views.crud import NgCRUDView
from django_remote_forms.forms import RemoteForm
from rest_framework.views import APIView
from rest_framework.response import Response

from . import encoders, register, SlickModelViewSet
from .registery import NotRegistered


class Home(TemplateView):
    template_name = "slick/home.html"



"""
class App(View, JSONResponseMixin):
    def app_dict(self):
        request = self.request
        app_dict = {}
        user = request.user

        for model, model_admin in site._registry.items():
            app_label = model._meta.app_label
            app_label, model_name = str(model._meta).split('.');
            has_module_perms = user.has_module_perms(app_label)
            
            if has_module_perms:
                perms = model_admin.get_model_perms(request)
                
                if True in perms.values():
                    list_display = {}

                    for i, field_name in enumerate(model_admin.list_display):
                        text, attr = label_for_field(field_name, model_admin.model,
                            model_admin = model_admin,
                            return_attr = True
                        )
                        list_display[field_name] = text

                    model_dict = {
                        'name': force_text(model._meta.verbose_name_plural),
                        'admin_url': mark_safe('/admin/%s/%s/' % (app_label, model.__name__.lower())),
                        'perms': perms,
                        'description': model_admin.description if hasattr(model_admin, 'description') else None,
                        'model': model_name,
                        'list_display': list_display,
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
                            'app_label': app_label,
                        }
        #print app_dict     

        return app_dict

    def get_context_data(self, **kwargs):
        app_dict = self.app_dict()
        #print app_dict

        if 'app_label' in kwargs:
            data = app_dict[kwargs['app_label']]
            if "model" in kwargs:
                for m in data['models']:
                    if m['model'] == kwargs['model']:
                        data = m
                        break


        else:
            app_list = app_dict.values()
            app_list.sort(lambda x, y: cmp(x['name'], y['name']))
            data = app_list
        
        context = data
        return context
"""

# TODO add caching, permissions
class SlickAppView(APIView):
    def get(self, request, *args, **kwargs):
        #print kwargs
        applications = ['auth', 'budofit']

        if 'app_label' in kwargs:
            applications = [kwargs['app_label']]

        ''''
        app_dict = [ 
            sorted({
                'name': model.__name__,
                'verbose': model._meta.verbose_name_plural.title(),
            } for model in get_models(get_app(application)))
            for application in applications
        ]
        '''
        
        app_list = []
        for application in applications:
            app_dict = {}
            app = get_app(application)
            app_dict['app_label'] = application
            app_dict['name'] = application.title()
            app_dict['models'] = [{'name': model.__name__.lower(), "plural": model._meta.verbose_name_plural} for model in get_models(app)]
            app_list.append(app_dict)

        if 'app_label' in kwargs:
            return Response(app_list[0])

        return Response(app_list)


class SlickSettingsView(APIView):
    def get(self, request, *args, **kwargs):
        settings_dict = {
            "STATIC_URL": staticfiles_storage.url('')
        }

        return Response(settings_dict)


def model_router(request, app_label=None, model=None, pk=None):
    if app_label and model:
        try:
            model_class = ContentType.objects.get(app_label=app_label, model=model).model_class()
        except:
            raise

        if register.is_registered(model_class):
            slick_instance = register.get_from_register(model_class)
        else:
            raise NotRegistered('The model %s is not registered' % model_class.__name__)

        return SlickModelViewSet.as_view()



