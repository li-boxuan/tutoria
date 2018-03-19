"""View for search results."""
from django.views.generic import ListView, TemplateView
import re  # Regular expression for search matching
from django.db.models import Max

from account.models import Tutor
from scheduler.models import Session

from datetime import datetime, timedelta


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
    minPrice = 0  # Integer. Minimum hourly rate.
    price_limit = 1000
    maxPrice = 500  # Integer. Maximum hourly rate.
    tutor_type = 'ALL'
    only_show_available = False  # Only show tutor with available session in the coming 7 days?

    def dispatch(self, request, *args, **kwargs):
        self.price_limit = list(Tutor.objects.all().aggregate(Max('hourly_rate')).values())[0]
        self.maxPrice = self.price_limit
        return super(ResultView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Determine the list of tutors to be displayed."""
        if 'keywords' in self.request.GET:
            self.keywords = self.request.GET['keywords']
        if 'sort' in self.request.GET:
            self.sort_method = self.request.GET['sort']
        if 'minPrice' in self.request.GET:
            self.minPrice = int(re.sub("\D", "", self.request.GET['minPrice']))
        if 'maxPrice' in self.request.GET:
            self.maxPrice = int(re.sub("\D", "", self.request.GET['maxPrice']))
        if 'tutor_type' in self.request.GET:
            self.tutor_type = self.request.GET['tutor_type']
        if 'only_show_available' in self.request.GET:
            self.only_show_available = eval(self.request.GET['only_show_available'])
        if 'price_limit' in self.request.GET:
            self.price_limit = self.request.GET['price_limit']

        all_tutors = Tutor.objects.filter(visible=True)  # Obtain visible tutors
        filtered_tutors = []
        if len(self.keywords) == 0:
            filtered_tutors = all_tutors
        else:
            # Filter according to keywords
            for tutor in all_tutors:
                # Search query in full name
                tutor_info = tutor.full_name
                # Search query in courses
                for course in tutor.courses.all():
                    tutor_info += (" " + str(course))
                # Search query in tags
                for tag in tutor.tags.all():
                    tutor_info += (" " + str(tag))
                # Search query in university
                tutor_info += (" " + tutor.university)
                # Regular expression match
                for keyword in self.keywords.split():
                    if re.search(keyword, tutor_info, re.IGNORECASE) and tutor not in filtered_tutors:
                        filtered_tutors.append(tutor)
        # Filter according to hourly rate range.
        filtered_tutors = [t for t in filtered_tutors if
                           self.minPrice <= t.hourly_rate <= self.maxPrice]
        # Filter according to tutor type
        if self.tutor_type != 'ALL':
            filtered_tutors = [t for t in filtered_tutors if t.tutor_type == self.tutor_type]
        if self.only_show_available:
            filtered_tutors = [t for t in filtered_tutors if tutor_available(t)]
        # Sort tutors
        if self.sort_method == 'hourly_rate_inc':
            return sorted(filtered_tutors, key=lambda x: x.hourly_rate, reverse=False)
        if self.sort_method == 'hourly_rate_dec':
            return sorted(filtered_tutors, key=lambda x: x.hourly_rate, reverse=True)
        return sorted(filtered_tutors, key=lambda x: x.avgRating, reverse=True)

    def get_context_data(self, **kwargs):
        """Obtain search query keywords from GET request."""
        context = super(ResultView, self).get_context_data(**kwargs)
        if 'keywords' in self.request.GET:
            context['keywords'] = self.request.GET['keywords']
        else:
            context['keywords'] = self.keywords
        # print('keywords ==> ' + context['keywords'])
        context['sort'] = self.sort_method
        context['minPrice'] = self.minPrice
        context['tutor_type'] = self.tutor_type
        context['only_show_available'] = self.only_show_available
        context['price_limit'] = self.price_limit
        context['maxPrice'] = self.maxPrice
        return context


def tutor_available(tutor):
    """Test if tutor has any available session in the coming 7 days."""
    today_min = datetime.combine(datetime.today(), datetime.min.time())
    future_max = datetime.combine(datetime.today() + timedelta(7), datetime.max.time())
    available_sessions = Session.objects.filter(tutor=tutor, status='A', start_time__gte=today_min,
                                                end_time__lte=future_max)
    return available_sessions.count() > 0
