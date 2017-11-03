"""Views for the Tutor App."""
from __future__ import print_function
from django.shortcuts import (get_object_or_404, render, render_to_response,
                              redirect)
from django.http import HttpResponse
<< << << < HEAD
from account.models import Tutor, Student, User
from scheduler.models import Session, BookingRecord
from django.contrib.auth.decorators import login_required
from datetime import datetime
from wallet.models import Transaction


def detail(request, tutor_id):
    """View for rendering a detailed profile of a tutor."""
    tutor = get_object_or_404(Tutor, id=tutor_id)
    # try:
    #    username = request.session['username']
    # except FieldError:
    #    pass
    # if username is not None:
    #    student = Student.objects.get(username=username)
    #    for record in student.bookingrecord_set.all():
    #        pass
    return render(request, 'detail.html', {'tutor': tutor})


>>>>>> > 85157c6013b48fa52b6f26ea4aee66501d85ab55

# -----------------------------------------------------------------------------
# ####### Book Session #######


@login_required(login_url='/auth/login/')
def confirm_booking(request, tutor_id):
    """Confirm booking a new session."""
    if request.method == 'POST':
        user = User.objects.get(username=request.session['username'])
        student = Student.objects.get(user=user)
        tutor = Tutor.objects.get(pk=tutor_id)
        session = Session.objects.get(pk=request.POST.get('session_id', ''))
        # Ignore commission for now because it might be saved by coupon.
        if (student.wallet_balance - tutor.hourly_rate) < 0:
            # TODO: beautify
            return HttpResponse("You don't have enough money.")
        if (tutor.username == student.username):
            # TODO: beautify
            return HttpResponse("You can't book your session.")
        # if (student.bookingrecord_set.all().filter(
        #    entry_date__date  = session.start_time.date).exists()):
        #    return HttpResponse("You can only book one session per day!")
        return render(request, 'book.html', {'tutor': tutor,
                                             'session': session})


@login_required(login_url='/auth/login/')
def save_booking(request, tutor_id):
    """Save booking record and redirect to the dashboard."""
    if request.method == 'POST':
        username = request.session['username']
        user = User.objects.get(username=username)
        student = Student.objects.get(user=user)
        session_id = request.POST.get('session_id', '')
        tutor = Tutor.objects.get(pk=tutor_id)
        session = Session.objects.get(pk=session_id)
        # TODO: mark session as selected
        if not session.status == session.BOOKABLE:
            # TODO: handle exception
            # return
            pass
        # added following lines for testing.  - Jiayao
        session.tutor = tutor
        session.status = session.BOOKED
        session.save()

        now = datetime.now()
        # TODO: check balance and other assertions
        # TODO: django add timezone to naive datetime  - Jiayao
        # TODO: handle coupons
        # TODO: make change to the user balance
        # TODO: check today
        transaction = Transaction(issuer=student, receiver=tutor,
                                  amount=tutor.hourly_rate,
                                  created_at=now,
                                  commission=tutor.hourly_rate * 0.05)
        transaction.save()
        student.wallet_balance -= tutor.hourly_rate
        bookRecord = BookingRecord(
            tutor=tutor, student=student, session=session, entry_date=now,
            transaction=transaction)
        student.wallet_balance -= tutor.hourly_rate * \
            (0.5 if tutor.tutor_type == 'CT' else 1)
        bookRecord.save()
        return redirect("/dashboard/mybookings/")
    else:
        return HttpResponse("not a POST request!")

# -----------------------------------------------------------------------------
