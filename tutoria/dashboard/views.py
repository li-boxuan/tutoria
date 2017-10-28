from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from account.models import (User,Tutor, Student)


class MybookingsView(generic.ListView):
    model = Account
    template_name = 'dashboard.html'
    context_object_name = 'mybookings'
