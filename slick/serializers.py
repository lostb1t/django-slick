from rest_framework import pagination
from rest_framework import serializers
from rest_framework.decorators import list_route


class BaseModelSerializer(serializers.ModelSerializer):
    pass


#ModelPostSerializer()