from django.conf.urls import url

from . import views

app_name = 'dashboard'

urlpatterns = [
    # url(r'debug$', views.debug, name='debug'),
    url(r'mybookings$', views.MybookingsView, name='mybookings'),

]
