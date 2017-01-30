from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success),
    url(r'^add_appointment/(?P<id>\d+)$', views.add_appointment),
    url(r'^delete/(?P<id>\d+)/(?P<aid>\d+)$', views.delete),
    url(r'^appointments$', views.appointments),
    url(r'^update/(?P<id>\d+)$', views.update)
]
