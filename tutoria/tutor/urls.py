'""URL Mapping.""'

from django.conf.urls import url
from . import views

app_name = 'tutor'

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<tutor_id>[0-9]+)/book/$',
        views.confirm_booking, name='confirm_booking'),
    url(r'^(?P<tutor_id>[0-9]+)/book/confirm$',
        views.save_booking, name='save_booking'),
    url(r'^(?P<tutor_id>[0-9]+)/review$',
        views.ReviewView.as_view(), name='review'),
]
