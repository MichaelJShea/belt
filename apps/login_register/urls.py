from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.show_login),
    url(r'^login$', views.login),
    url(r'^signup$', views.show_registration),
    url(r'^register$', views.register_user),
    url(r'^register_user$', views.register_user),
    url(r'^success$', views.success),
]