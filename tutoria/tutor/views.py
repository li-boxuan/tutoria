"""Views for the Tutor App."""
from __future__ import print_function
from django.shortcuts import (get_object_or_404, render, render_to_response,
                              redirect)
from django.http import HttpResponse

from account.models import Tutor, Student, User
from scheduler.models import Session
from django.contrib.auth.decorators import login_required


def detail(request, tutor_id):
    """View for rendering a detailed profile of a tutor."""
    tutor = get_object_or_404(Tutor, id=tutor_id)
    return render(request, 'detail.html', {'tutor': tutor})

# -----------------------------------------------------------------------------
# ####### Book Session #######


@login_required
def book_session(request, tutor_id):
    """Confirm booking a new session."""
    if request.method == 'POST':
        username = request.session['username']
        if username is not None:  # If the user has logged in
            user = User.objects.get(username=username)
	    student = Student.objects.get(user=user)
            session_id = request.POST.get('session_id', '')
            tutor = Tutor.objects.get(pk=tutor_id)
            session = Session.objects.get(pk=session_id)
            # Ignore commission for now because it might be saved by coupon
            if (student.wallet_balance - tutor.hourly_rate) < 0:
                return HttpResponse("You don't have enough money.")
            if (tutor.username == student.username):
                return HttpResponse("You can't book your session.")
            if (student.bookingrecord_set.all().exists()):
                return HttpResponse("You can only book one session per day!")
            return render(request, 'book.html', {'tutor': tutor,
                                                 'session': session})


def save_booking(request, tutor_id):
    """Save booking record and redirect to the dashboard."""
    if request.method == 'POST':
        return HttpResponse("received the request!")
    else:
        return HttpResponse("not a POST request!")

# -----------------------------------------------------------------------------
