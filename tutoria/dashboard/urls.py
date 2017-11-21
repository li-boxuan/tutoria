from django.conf.urls import url

from . import views

app_name = 'dashboard'

urlpatterns = [
    url(r'mybookings/$', views.MybookingsView.as_view(), name='mybookings'),
    url(r'mytransactions/$',views.MytransactionsView.as_view(), name='mytransactions'),
    url(r'mytimetable/$',views.MyTimetableView.as_view(), name='myTimetable'),
]
