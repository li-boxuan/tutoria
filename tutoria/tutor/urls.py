"""URL Mapping."""

from django.conf.urls import url
from . import views

app_name = 'tutor'

urlpatterns = [
    # url(r'^(?P<id>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<tutor_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<tutor_id>[0-9]+)/book$', views.BookView.as_view(), name='book'),
]
