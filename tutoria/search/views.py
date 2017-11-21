"""View for search results."""
from django.views.generic import ListView, TemplateView
import re  # Regular expression for search matching

from account.models import Tutor


class IndexView(TemplateView):
    """Render the search page."""

    template_name = 'search.html'
    context_object_name = 'index_context'


class ResultView(ListView):
    """View for search results."""

    template_name = 'result.html'
    model = Tutor
    sort_method = 'rating'  # Sort by rating by default
    keywords = ''
    minPrice = 0  # Integer
    maxPrice = 500  # Integer

    def get_queryset(self):
        """Determine the list of tutors to be displayed."""
        print(self.request.GET)
        if 'keywords' in self.request.GET:
            self.keywords = self.request.GET['keywords']
        if 'sort' in self.request.GET:
            self.sort_method = self.request.GET['sort']
        if 'minPrice' in self.request.GET:
            self.minPrice = int(re.sub("\D", "", self.request.GET['minPrice']))
        if 'maxPrice' in self.request.GET:
            self.maxPrice = int(re.sub("\D", "", self.request.GET['maxPrice']))
        all_tutors = Tutor.objects.all()  # Obtain unfiltered results
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
            if re.search(self.keywords, tutor_info, re.IGNORECASE):
                filtered_tutors.append(tutor)
        # Filter according to hourly rate range.
        filtered_tutors = [t for t in filtered_tutors if
                           self.minPrice <= t.hourly_rate <= self.maxPrice]
        if self.sort_method == 'hourly_rate':
            return sorted(filtered_tutors, key=lambda x: x.hourly_rate, reverse=False)
        return sorted(filtered_tutors, key=lambda x: x.avgRating, reverse=True)

    def get_context_data(self, **kwargs):
        """Obtain search query keywords from GET request."""
        context = super(ResultView, self).get_context_data(**kwargs)
        if 'keywords' in self.request.GET:
            context['keywords'] = self.request.GET['keywords']
        else:
            context['keywords'] = self.keywords
        context['sort'] = self.sort_method
        context['minPrice'] = self.minPrice
        context['maxPrice'] = self.maxPrice
        return context
