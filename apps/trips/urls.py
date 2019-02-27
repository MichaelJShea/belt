from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^trips$', views.show_trips),
    url(r'^trips/new', views.show_create_new_trip),
    url(r'^trips/create', views.create_trip),
    url(r'trips/remove/(?P<id>\d+)$', views.remove_trip),
    url(r'trips/view/(?P<id>\d+)$', views.view_trip),
    url(r'trips/edit/(?P<id>\d+)$', views.show_edit_trip),
    url(r'trips/join/(?P<id>\d+)$', views.join_trip),
    url(r'trips/cancel/(?P<id>\d+)$', views.cancel),
    url(r'trips/edit$', views.edit_trip),
    url(r'^logout', views.logout),
]