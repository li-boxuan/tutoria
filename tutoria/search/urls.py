from django.conf.urls import url

from . import views

app_name = ['search']

urlpatterns = [
    # url(r'debug$', views.debug, name='debug'),
    url(r'result$', views.ResultView.as_view(), name='result'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    
]
