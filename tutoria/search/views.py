from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from account.models import Tutor


class IndexView(generic.TemplateView):
    template_name = 'search.html'
    # context_object_name = 'index_context'


class ResultView(generic.ListView):
    """View for search results."""
    model = Tutor
    template_name = 'result.html'
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        """Obtain search query keywords from GET request."""
        context = super(ResultView, self).get_context_data(**kwargs)
        context['keywords'] = self.request.GET['keywords']
        print(self.request.GET['keywords'])
        return context
