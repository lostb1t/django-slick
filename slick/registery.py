
from django.contrib.auth.models import User, Group
from django.utils import six

from rest_framework import routers

from . import SlickModelViewSet


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class SlickRegister(object):
    def __init__(self):
        self._registry = {}  # model_class class -> slick_class

    def register(self, model, slick_class=None, **options):
        if not slick_class:
            class Meta:
                pass

            setattr(Meta, 'model', model)
            attrs = {
                '__module__': __name__,
                'Meta': Meta,
                'model': model,
            }
            name = model.__name__
            slick_class = type('SlickModel%sViewSet' % name, (SlickModelViewSet,), attrs)

        if model in self._registry:
            raise AlreadyRegistered('The model %s is already registered' % model.__name__)


        self._registry[model] = slick_class
        #print self._registry

    def is_registered(self, model):
        """
        Check if a model class is registered.
        """
        return model in self._registry

    def get_from_register(self, model):
        return self._registry[model]

    def get_urls(self):
        router = routers.SimpleRouter()

        for model, slick_class in six.iteritems(self._registry):
            #print type(slick_class)
            #slick_class.model = model
            #print slick_class.model
            router.register(r'api/%s/%s' % (model._meta.app_label, model.__name__.lower()), slick_class, model.__name__.lower())
        
        return router.urls


register = SlickRegister()


register.register(User)
register.register(Group)
