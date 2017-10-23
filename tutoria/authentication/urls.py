"""
authentication/urls.py

Created on Oct. 23, 2017
by Jiayao
"""
from django.conf.urls import url

from . import views

app_name = 'authentication'

urlpatterns = [
      url(r'^$', views.SignupView.as_view(), name='signup'),
]
