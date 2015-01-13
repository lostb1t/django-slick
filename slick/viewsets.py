from django.utils.encoding import force_text
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.renderers import HTMLFormRenderer, StaticHTMLRenderer
from rest_framework.decorators import list_route, detail_route, renderer_classes, api_view
from rest_framework.compat import OrderedDict
from rest_framework.utils.field_mapping import ClassLookupDict

from .serializers import *


class MultiSerializerViewSetMixin(object):
    def get_serializer_class(self):
        """
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:

        class MyViewSet(ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }

            @action
            def my_action:
                ...

        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.

        """
        print "action"
        #print self.action
        if hasattr(self, 'action'):
            try:
                return self.serializer_action_classes[self.action]
            except KeyError:
                pass

        return super(MultiSerializerViewSetMixin, self).get_serializer_class()


schema_type_lookup = ClassLookupDict({
    serializers.Field: 'string', # todo
    serializers.BooleanField: 'boolean',
    serializers.CharField: 'string',
    serializers.URLField: 'url',
    serializers.EmailField: 'string',
    serializers.RegexField: 'regex',
    serializers.SlugField: 'slug',
    serializers.IntegerField: 'number',
    serializers.FloatField: 'float',
    serializers.DecimalField: 'decimal',
    serializers.DateField: 'string',    # need to build date support, html5?
    serializers.DateTimeField: 'string', # need to build datetime support, html5?
    serializers.TimeField: 'string', # need to build time support, html5?
    serializers.ChoiceField: 'choice',
    serializers.MultipleChoiceField: 'multiple choice',
    serializers.FileField: 'file upload',
    serializers.ImageField: 'image upload',
})

field_type_lookup = ClassLookupDict({
    serializers.Field: 'string', # todo
    serializers.BooleanField: 'boolean',
    serializers.CharField: 'string',
    serializers.URLField: 'url',
    serializers.EmailField: 'string',
    serializers.RegexField: 'regex',
    serializers.SlugField: 'slug',
    serializers.IntegerField: 'number',
    serializers.FloatField: 'float',
    serializers.DecimalField: 'decimal',
    serializers.DateField: 'string',    # need to build date support, html5?
    serializers.DateTimeField: 'string', # need to build datetime support, html5?
    serializers.TimeField: 'string', # need to build time support, html5?
    serializers.ChoiceField: 'choice',  #todo
    serializers.MultipleChoiceField: 'multiple choice', #todo
    serializers.FileField: 'file upload',
    serializers.ImageField: 'image upload',
})


# TODO add several options. Like list fields, exclude fields etc. Similair to ModelAdmin
# TODO put several functionality in mixins. Like the Schema generator
class SlickModelViewSet(viewsets.ModelViewSet):
    model = None
    
    def get_serializer_class(self):
        print "class"
        serializer_class = self.serializer_class
        if serializer_class is not None:
            return serializer_class

        assert self.model is not None, \
            "'%s' should either include a 'serializer_class' attribute, " \
            "or use the 'model' attribute as a shortcut for " \
            "automatically generating a serializer class." \
            % self.__class__.__name__

        name = self.model.__name__
        #print self.action
        class Meta:
            model = self.model
            if self.action == "list":
                fields = ('pk', '__unicode__',)

        attrs = {
            '__module__': name,
            'Meta': Meta,
        }

        return type('Default%sSerializer' % name, (SlickModelSerializer,), attrs)

    def get_queryset(self):
        if not self.queryset and self.model:
            self.queryset = self.model.objects.all()

        return super(SlickModelViewSet, self).get_queryset()
    '''
    @detail_route(methods=['GET'])
    def form(self, request, pk=None):
        response = {}
        response['form'] = HTMLFormRenderer().render(self.get_serializer(self.get_object()).data, renderer_context={'request': request})
        return Response(response)

    @list_route(methods=['GET'])
    def create_form(self, request, pk=None):
        response = {}
        response['form'] = HTMLFormRenderer().render(self.get_serializer().data, renderer_context={'request': request})
        return Response(response)
    '''
    @list_route(methods=['GET'])
    def form(self, request):
        serializer = self.get_serializer()
        definition = self.get_form_definition(serializer)
        return Response(definition)

    @list_route(methods=['GET'])
    def schema(self, request):
        """ Returns model schema, based on formly """
        serializer = self.get_serializer()
        schema = {
          "type": "object",
          "title": "test",
        }
        schema['properties'] = self.get_schema_properties(serializer)
        schema['required'] = self.schema_required_fields(serializer)
        return Response(schema)

    def get_form_definition(self, serializer):
        """
        Given an instance of a serializer, return a form definition.
        """
        if hasattr(serializer, 'child'):
            # If this is a `ListSerializer` then we want to examine the
            # underlying child serializer instance instead.
            serializer = serializer.child
        
        definition = []
        for field_name, field in serializer.fields.items():
            field_def = {"key": field_name, "type": field_type_lookup[field]}
            style = getattr(field, 'style', None)
            if style is not None:
                if 'input_type' in style:
                    field_def['type'] = style['input_type']
            definition.append(field_def)

        return definition

    def schema_required_fields(self, serializer):
        return [
            field_name
            for field_name, field in serializer.fields.items() if getattr(field, 'required', None)
        ]        

    def get_schema_properties(self, serializer):
        """
        Given an instance of a serializer, return a schema about its fields.
        """
        if hasattr(serializer, 'child'):
            # If this is a `ListSerializer` then we want to examine the
            # underlying child serializer instance instead.
            serializer = serializer.child
        return OrderedDict([
            (field_name, self.get_schema_field(field))
            for field_name, field in serializer.fields.items()
        ])

    def get_schema_field(self, field):
        """
        Given an instance of a serializer field, return a dictionary
        of metadata about it.
        """
        field_info = OrderedDict()
        #field_info['key'] = field_name
        field_info['type'] = schema_type_lookup[field]
        field_info['description'] = getattr(field, 'help_text', None)
        field_info['title'] = getattr(field, 'label', None)
        
        '''
        style = getattr(field, 'style', None)
        if style is not None:
            if 'input_type' in style:
                field_info['type'] = style['input_type']
        choices = getattr(field, 'choices', None)
        '''
        #if choices is not None
        #print getattr(field, 'choices', None)
            #print getattr(field, 'style', None)

        #field_info['min'] = getattr(field, 'min_length', None)
        #field_info['max'] = getattr(field, 'max_length', None)

        '''
        for attr in ['read_only', 'label',]:
            value = getattr(field, attr, None)
            if value is not None and value != '':
                field_info[attr] = force_text(value, strings_only=True)
        '''
        
        '''
        if hasattr(field, 'choices'):
            field_info['choices'] = [
                {
                    'value': choice_value,
                    'display_name': force_text(choice_name, strings_only=True)
                }
                for choice_value, choice_name in field.choices.items()
            ]
        '''

        return field_info



class SlickUserViewSet(MultiSerializerViewSetMixin, SlickModelViewSet):
    serializer_class = SlickUserModelSerializer
    queryset = get_user_model().objects.all()
    serializer_action_classes = {
       'list': SlickUserModelListSerializer,
    }

