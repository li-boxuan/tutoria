from django.conf.urls import url

from . import views

app_name = 'dashboard'

urlpatterns = [
    # url(r'debug$', views.debug, name='debug'),
    url(r'dashboard/$', views.MybookingsView.as_view(), name='dashboard'),

]
