"""URL Mapping."""

from django.conf.urls import url
from . import views

app_name = 'tutor'

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # Old version
    # url(r'^(?P<tutor_id>[0-9]+)/book$',
    # views.BookView.as_view(), name='book'),
    url(r'^(?P<tutor_id>[0-9]+)/book/$',
        views.confirm_booking, name='confirm_booking'),
    url(r'^(?P<tutor_id>[0-9]+)/book/confirm$',
        views.save_booking, name='save_booking'),
]
