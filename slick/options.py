from rest_framework import serializers


class ModelSlick(object):
    model = None
    serializer = serializers.ModelSerializer
    fields = None