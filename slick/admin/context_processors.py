from django.apps import apps

def slick(request):
    return {'apps': apps.get_app_configs() }
