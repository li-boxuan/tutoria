"""
authentication/urls.py

Created on Oct. 23, 2017
by Jiayao
"""
from django.conf.urls import url

from . import views

app_name = 'auth'

urlpatterns = [
      url(r'^$', views.IndexView.as_view(), name='signup'),
      url(r'^student/$', views.StudentView.as_view(), name='student'),
      url(r'^tutor/$', views.TutorView.as_view(), name='tutor'),
      url(r'^both/$', views.BothView.as_view(), name='both'),
      url(r'^login/$', views.LoginView.as_view(), name='login'),
      url(r'^logout/$', views.logout_view, name='logout')
]
