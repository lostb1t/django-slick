from django.conf.urls import include, patterns, url
from django.contrib import admin

from . import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.Home.as_view(), name='home'),
    url(r'^api/app/$', views.AppAPIView.as_view(), name='app_list'),
    url(r'^api/app/(?P<app_label>[a-zA-Z0-9-_]+)/$', views.AppAPIView.as_view(), name='app_detail_list'),
	url(r'^api/app/(?P<app_label>[a-zA-Z0-9-_]+)/(?P<model>[a-zA-Z0-9-_]+)/', views.AppAPIView.as_view(), name='app_model_detail'),
    
    url(r'^api/model/(?P<app_label>[a-zA-Z0-9-_]+)/(?P<model>[a-zA-Z0-9-_]+)/$', views.ModelAdminAPIView.as_view(), name='model_list'),
    url(r'^api/model/(?P<app_label>[a-zA-Z0-9-_]+)/(?P<model>[a-zA-Z0-9-_]+)/(?P<pk>[a-zA-Z0-9-_]+)/$', views.ModelAdminAPIView.as_view(), name='model_detail'),
)