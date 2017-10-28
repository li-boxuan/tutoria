"""tutoria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from __future__ import (absolute_import, print_function)
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^$', views.IndexView.as_view(), name='homepage'),
    url(r'^search/', include('search.urls', namespace='search'), name='search'),
    url(r'^tutor/', include('tutor.urls', namespace='tutor'), name='tutor'),
    # app_name: authentication namespace: auth
    url(r'^auth/', include('authentication.urls', namespace='auth'), name='auth'),
    url(r'^dashboard/',include('dashboard.urls', namespace='dashboard'), name='dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

