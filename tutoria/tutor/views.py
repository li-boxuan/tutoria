"""Views for the Tutor App."""
from __future__ import print_function
from django.shortcuts import (get_object_or_404, render, render_to_response,
                              redirect)
from django.views import generic
from django.template import RequestContext
from .forms import BookForm
from django.http import HttpResponse

from account.models import Tutor


def detail(request, tutor_id):
    """View for rendering a detailed profile of a tutor."""
    tutor = get_object_or_404(Tutor, id=tutor_id)
    return render(request, 'detail.html', {'tutor': tutor})

# -----------------------------------------------------------------------------
# ####### Book Session #######


# # New experimental version
def book_session(request, tutor_id):
    """Book a new session."""
    if request.method == 'POST':
        return HttpResponse("receive POST request!")
        # if form.is_valid():
        # booking = form.save(commit=False)
        # # Save some other hidden attributes
        # booking.save()
        # return redirect('detail', tutor_id)
    else:
        return HttpResponse("In ELSE")
    # return render(request, 'book.html', {'form': form})

# -----------------------------------------------------------------------------
