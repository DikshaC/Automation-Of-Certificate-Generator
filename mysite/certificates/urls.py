from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from . import views
urlpatterns = [
    url(r'^$', views.login),
    url(r'^home/$', views.home),
    url(r'^home/add_user/$', views.add_user),
    url(r'^home/edit_user/$', views.edit_user),
    url(r'^home/view_user/$', views.view_user),
    url(r'^home/add_certificate/$', views.add_certificate),
    url(r'^home/edit_certificate/$', views.edit_certificate),
    url(r'^home/view_certificate/$', views.view_certificate),
    url(r'^home/add_event/$', views.add_event),
    url(r'^home/edit_event/$', views.edit_event),
    url(r'^home/view_event/$', views.view_event),
    url(r'^home/organise_event/$', views.organise_event),
    url(r'^home/edit_organised_event/$', views.edit_organised_event),
    url(r'^home/view_organised_event/$', views.view_organised_event),
]