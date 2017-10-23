from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

class IndexView(generic.TemplateView):
    template_name = 'index.html'
    # context_object_name = 'index_context'
