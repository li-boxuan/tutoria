"""Views for the Tutor App."""
from __future__ import print_function
from django.shortcuts import (get_object_or_404, render, render_to_response,
                              redirect)
from django.http import HttpResponse
from django.views import generic

from account.models import Tutor, Student, User
from scheduler.models import Session, BookingRecord
from django.contrib.auth.decorators import login_required
from scheduler.models import BookingRecord
from datetime import datetime, date
from wallet.models import Transaction


class DetailView(generic.DetailView):
    model = Tutor
    template_name = 'detail.html'
    context_object_name = 'tutor'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['phone_visible'] = False
        if self.request.user.is_authenticated:
            visitor = User.objects.get(
                username=self.request.session['username'])
            # check if current visitor is the tutor itself
            if visitor == self.get_object().user:
                context['phone_visible'] = True
            # check if current visitor has booked this tutor's session
            for record in self.get_object().bookingrecord_set.all():
                if visitor == record.student.user:
                    context['phone_visible'] = True
        return context


# -----------------------------------------------------------------------------
# ####### Book Session #######


@login_required(login_url='/auth/login/')
def book_session(request, tutor_id):
    """Confirm booking a new session."""
    if request.method == 'POST':
        username = request.session['username']  # Won't work if not logged in
        if username is not None:  # If the user has logged in
            user = User.objects.get(username=username)
            student = Student.objects.get(user=user)
            session_id = request.POST.get('session_id', '')
            tutor = Tutor.objects.get(pk=tutor_id)
            session = Session.objects.get(pk=session_id)
            # Ignore commission for now because it might be saved by coupon
            if (student.wallet_balance - tutor.hourly_rate) < 0:
                return HttpResponse("Your balance is " +
                                    str(student.wallet_balance) +
                                    ". You don't have enough money.")
            if (tutor.username == student.username):
                return HttpResponse("You can't book your session.")
            if not student.bookingrecord_set.all().filter(
                    entry_date__date=date.today()).empty():

                return HttpResponse("You can only book one session per day!")
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
        transaction = Transaction(issuer=student, receiver=tutor,
                                  amount=tutor.hourly_rate,
                                  created_at=now,
                                  commission=tutor.hourly_rate * 0.05)
        transaction.save()
        bookRecord = BookingRecord(
            tutor=tutor, student=student, session=session, entry_date=now,
            transaction=transaction)
        bookRecord.save()
        return redirect("/dashboard/mybookings/")
    else:
        return HttpResponse("not a POST request!")

# -----------------------------------------------------------------------------
