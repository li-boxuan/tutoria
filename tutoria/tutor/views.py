from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from account.models import (User, Tutor)

class DetailView(generic.TemplateView):
    template_name = 'result.html'

