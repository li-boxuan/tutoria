from django.conf.urls import url

from . import views

app_name = 'tutor'

urlpatterns = [
    url(r'^(?P<id>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
]
