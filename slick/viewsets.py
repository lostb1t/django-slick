from django.utils.encoding import force_text

from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route
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

        if hasattr(self, 'action'):
            try:
                return self.serializer_action_classes[self.action]
            except KeyError:
                pass

        return super(MultiSerializerViewSetMixin, self).get_serializer_class()


label_lookup = ClassLookupDict({
    serializers.Field: 'field',
    serializers.BooleanField: 'checkbox',
    serializers.CharField: 'text',
    serializers.URLField: 'url',
    serializers.EmailField: 'email',
    serializers.RegexField: 'regex',
    serializers.SlugField: 'slug',
    serializers.IntegerField: 'number',
    serializers.FloatField: 'float',
    serializers.DecimalField: 'decimal',
    serializers.DateField: 'date',
    serializers.DateTimeField: 'datetime',
    serializers.TimeField: 'time',
    serializers.ChoiceField: 'choice',
    serializers.MultipleChoiceField: 'multiple choice',
    serializers.FileField: 'file upload',
    serializers.ImageField: 'image upload',
})


# TODO add several options. Like list fields, exclude fields etc. Similair to ModelAdmin
# TODO put several functionality in mixins. Like the Schema generator
class SlickModelViewSet(viewsets.ModelViewSet, MultiSerializerViewSetMixin):
    def get_serializer_class(self):
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

        return type('Default%sSerializer' % name, (BaseModelSerializer,), attrs)

    def get_queryset(self):
        if not self.queryset and self.model:
            self.queryset = self.model.objects.all()

        return super(SlickModelViewSet, self).get_queryset()

    @list_route(methods=['GET'])
    def schema(self, request):
        """ Returns model schema, based on formly """
        serializer = self.get_serializer()
        schema = self.get_schema(serializer)        
        return Response(schema)

    def get_schema(self, serializer):
        """
        Given an instance of a serializer, return a dictionary of metadata
        about its fields.
        """
        if hasattr(serializer, 'child'):
            # If this is a `ListSerializer` then we want to examine the
            # underlying child serializer instance instead.
            serializer = serializer.child
        return [
            self.get_schema_field(field_name, field)
            for field_name, field in serializer.fields.items()
        ]

    def get_schema_field(self, field_name, field):
        """
        Given an instance of a serializer field, return a dictionary
        of metadata about it.
        """
        field_info = OrderedDict()
        field_info['key'] = field_name
        field_info['type'] = label_lookup[field]
        field_info['disabled'] = getattr(field, 'read_only', False)
        field_info['required'] = getattr(field, 'required', False)
        field_info['description'] = getattr(field, 'help_text', None)
        #field_info['min'] = getattr(field, 'min_length', None)
        #field_info['max'] = getattr(field, 'max_length', None)


        for attr in ['read_only', 'label',]:
            value = getattr(field, attr, None)
            if value is not None and value != '':
                field_info[attr] = force_text(value, strings_only=True)
        
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

