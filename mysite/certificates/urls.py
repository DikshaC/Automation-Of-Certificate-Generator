from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from . import views
urlpatterns = [
    url(r'^$', views.login),
    url(r'^home/$',views.home),
    url(r'^login/$', login, {'template_name': 'certificates/login.html'}),
    url(r'^logout/$', logout, {'template_name': 'certificates/logout.html'}),
    url(r'^template/$', views.add_certificate),
    url(r'^event/$', views.add_event),
]