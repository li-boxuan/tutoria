"""View for search results."""
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView
import re  # Regular expression for search matching

from account.models import Tutor
from .forms import SearchForm


class IndexView(TemplateView):
    template_name = 'search.html'
    # context_object_name = 'index_context'


# class IndexView(FormView):
#     template_name = 'search.html'
#     form_class = SearchForm
#     success_url = '.'
#
#     def get_context_data(self, **kwargs):
#         context = super(IndexView, self).get_context_data(**kwargs)
#         return context
#
#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         # print "form is valid"
#         return super(IndexView, self).form_valid(form)


class ResultView(ListView):
    """View for search results."""

    template_name = 'result.html'
    model = Tutor

    def get_queryset(self):
        """Determine the list of tutors to be displayed."""
        keywords = self.request.GET['keywords']
        all_tutors = Tutor.objects.all()
        filtered_tutors = []
        for tutor in all_tutors:
            # Search query in full name
            tutor_info = tutor.full_name
            # Search query in courses
            for course in tutor.courses.all():
                tutor_info += (" " + str(course))
            # Search query in tags
            for tag in tutor.tags.all():
                tutor_info += (" " + str(tag))
            # Regular expression match
            if re.search(keywords, tutor_info, re.IGNORECASE):
                filtered_tutors.append(tutor)
        return sorted(filtered_tutors, key=lambda x: x.avgRating, reverse=True)

    def get_context_data(self, **kwargs):
        """Obtain search query keywords from GET request."""
        context = super(ResultView, self).get_context_data(**kwargs)
        context['keywords'] = self.request.GET['keywords']
        return context
