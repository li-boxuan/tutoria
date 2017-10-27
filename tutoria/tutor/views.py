"""Views for the Tutor App."""
from django.shortcuts import get_object_or_404, render, render_to_response
from django.views import generic
from django.template import RequestContext
from .forms import BookForm

from account.models import Tutor


def detail(request, tutor_id):
    """View for rendering a detailed profile of a tutor."""
    tutor = get_object_or_404(Tutor, id=tutor_id)
    return render(request, 'detail.html', {'tutor': tutor})

# -----------------------------------------------------------------------------
# ####### Book Session #######

# # Old version. Working but shitty.
# class BookView(generic.edit.FormView):
#     """Book View (class version)."""
#
#     template_name = 'book.html'
#     form_class = BookForm
#     # success_url = '/thanks/'


# # New experimental version
def book_session(request, tutor_id):
    """Book a new session."""
    form = BookForm
    return render(request, 'book.html', {'form': form})
#     context = RequestContext(request)
#
#     if request.method == 'POST':
#         form = BookForm(request.POST)
#         if form.is_valid():
#             form.save(commit=True)
# #            return index(request) # FIXME Call index() view, unavailable now
#         else:
#             print(form.errors)
#     return render_to_response('book.html', {'form': form}, context)

# -----------------------------------------------------------------------------
