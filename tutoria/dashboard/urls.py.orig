from django.conf.urls import url

from . import views

app_name = 'dashboard'

urlpatterns = [
    url(r'mybookings/$', views.MybookingsView.as_view(), name='mybookings'),
    url(r'mytransactions/$', views.MytransactionsView.as_view(), name='mytransactions'),
    url(r'mytimetable/$', views.MytimetableView.as_view(), name='mytimetable'),
    url(r'mywallet/$', views.MyWalletView.as_view(), name='mywallet'),
]
