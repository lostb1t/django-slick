from django.conf.urls import include, patterns, url
from django.contrib import admin

from . import views
from . import register

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.Home.as_view(), name='home'),
	url(r'^api/settings/$', views.SlickSettingsView.as_view(), name='settings'),
    url(r'^api/app/$', views.SlickAppView.as_view(), name='app-list'),
    url(r'^api/app/(?P<app_label>[a-zA-Z0-9-_]+)/$', views.SlickAppView.as_view(), name='app-detail'),
	url(r'^api/app/(?P<app_label>[a-zA-Z0-9-_]+)/(?P<model>[a-zA-Z0-9-_]+)/', views.SlickAppView.as_view(), name='app-model-detail'),
)


urlpatterns += register.get_urls()