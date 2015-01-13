#from django.contrib.auth import User
from django.conf import settings
from django.contrib.auth import get_user_model


from rest_framework import pagination
from rest_framework import serializers
from rest_framework.decorators import list_route


class SlickModelSerializer(serializers.ModelSerializer):
    pass


class SlickUserModelSerializer(SlickModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    class Meta:
        model = get_user_model()


class SlickUserModelListSerializer(SlickModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('pk', '__unicode__',)
