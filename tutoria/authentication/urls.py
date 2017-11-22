"""
authentication/urls.py

Created on Oct. 23, 2017
by Jiayao
"""
from django.urls import reverse, reverse_lazy
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
import functools as func

app_name = 'auth'

urlpatterns = [
      url(r'^$', views.IndexView.as_view(), name='signup'),
      # url(r'^tutor_profile/$', views.TutorSettingView.as_view(), name='tutor_profile'),
      url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
      url(r'^student/$', views.StudentView.as_view(), name='student'),
      url(r'^tutor/$', views.TutorView.as_view(), name='tutor'),
      url(r'^both/$', views.BothView.as_view(), name='both'),
      url(r'^login/$', views.LoginView.as_view(), name='login'),
      url(r'^logout/$', views.logout_view, name='logout'),
      url(r'^reset/$', lambda req, **kwargs: auth_views.password_reset(
		req, template_name='form.html',
        from_email=views.PASSWORD_EMAIL_SENDER,
        email_template_name='reset_password_email.html',
        post_reset_redirect=reverse_lazy('auth:password_reset_done'),
		extra_context={
            'validlink': True,
            'form_title': 'Forgot Password',
            'form_submit': 'Retreive Password',
        }, **kwargs
        ), name='password_reset'),
      url(r'^reset/retreive/$', lambda req, **kwargs: auth_views.password_reset_done(
		req, template_name='message.html',
        # post_reset_redirect='auth.password_reset_done',
		extra_context={
            'message_title': 'Forgot Password',
            'message_content': views.PASSWORD_RESET_DONE_MSG,
        }, **kwargs
        ), name='password_reset_done'),
      url(views.PASSWORD_RESET_TOKEN_REGEX, lambda req, **kwargs: auth_views.password_reset_confirm(
              req, template_name='form.html',
              post_reset_redirect=reverse_lazy('auth:password_reset_complete'),
              extra_context={
                  'form_title': 'Reset Password',
                  'form_submit': 'Reset',
                  'exception_msg': views.PASSWORD_RESET_EX_MSG,
              }, **kwargs
          ), name='password_reset_confirm'),
    url(r'^reset/done/$', lambda req, **kwargs : auth_views.password_reset_complete(
        req, template_name='message.html',
        extra_context={
            'message_title': 'Reset Password',
            'message_content': views.PASSWORD_RESET_COMPLETE,
        }, **kwargs
    ), name='password_reset_complete'),

]
