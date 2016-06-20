"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.userlogin, name='login'),
    url(r'^logout/$', views.userlogout, name='logout'),
    url(r'^archive/$', views.archive, name='archive'),
    url(r'^add/$', views.add, name='add'),
    url(r'^activity/(?P<activity_id>[0-9]+)/$', views.showactivity, name='showactivity'),
    url(r'^activity/(?P<activity_id>[0-9]+)/update/$', views.updateactivity, name='updateactivity'),
    url(r'^activity/(?P<activity_id>[0-9]+)/delete/$', views.deleteactivity, name='deleteactivity'),
    url(r'^activity/(?P<activity_id>[0-9]+)/startat/$', views.startactivityat, name='startactivityat'),
    url(r'^activity/(?P<activity_id>[0-9]+)/start/$', views.startactivity, name='startactivity'),
    url(r'^event/(?P<event_id>[0-9]+)/endat/$', views.endactivityat, name='endactivityat'),
    url(r'^event/(?P<event_id>[0-9]+)/end/$', views.endactivity, name='endactivity'),
    url(r'^event/(?P<event_id>[0-9]+)/update/$', views.updateevent, name='updateevent'),
    url(r'^event/(?P<event_id>[0-9]+)/delete/$', views.deleteevent, name='deleteevent'),
    url(r'^activity/(?P<activity_id>[0-9]+)/showevents/$', views.showevents, name='showevents'),
]
