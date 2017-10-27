"""Views for the Tutor App."""
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
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
    if request.method == 'POST':
        form = BookForm(request.POST)
        # if form.is_valid():
        # booking = form.save(commit=False)
        # # Save some other hidden attributes
        # booking.save()
        # return redirect('detail', tutor_id)
    else:
        form = BookForm()
    return render(request, 'book.html', {'form': form})

# -----------------------------------------------------------------------------
