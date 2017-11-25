"""Views for the Tutor App."""
from __future__ import print_function
from django.shortcuts import (render, redirect)
from django.http import HttpResponse

from account.models import Tutor, Student, User
from scheduler.models import Session, BookingRecord
from review.models import Review
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, timedelta, time
from django.utils import timezone
from wallet.models import Transaction
from django.views import generic
from django.core.mail import send_mail
from .forms import ReviewForm
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin


class DetailView(generic.DetailView):
    """A class for the detailed view of tutor profile."""

    model = Tutor
    template_name = 'detail.html'
    context_object_name = 'tutor'

    def get_context_data(self, **kwargs):
        """Get context data."""
        context = super(DetailView, self).get_context_data(**kwargs)
        # generate a 1D array which stores the timetable
        # there are 7 days
        # private tutor has 24 timeslots per day while contracted tutor has 48
        is_contracted_tutor = self.get_object().tutor_type == 'CT'
        slots_per_day = 48 if is_contracted_tutor else 24
        days_to_display = 7
        timetable = []
        # retrieve date of today
        today = date.today()
        
        now = datetime.now()
        if is_contracted_tutor:
            now_index = now.hour * 2 + now.minute // 30
        else:
            now_index = now.hour

        for i in range(days_to_display * slots_per_day):
            elem = {'status': 'X', 'date': str(today + timedelta(days=i / slots_per_day)), 'id': ''}
            # print(elem)
            timetable.append(elem)  # closed
        # print("tot: " + str(days_to_display * slots_per_day))
        # convert "date" of today to "datetime" of today's 0 'o clock
        # init_time = datetime.combine(today, datetime.min.time())
        for session in self.get_object().session_set.all():
            start_time = session.start_time
            start_time_of_the_day = timezone.make_aware(datetime.combine(start_time.date(), time(0, 0)))
            #print("start_time hour = ", start_time.hour, " start time of the day = ", start_time_of_the_day.hour)
            hour_diff = (start_time - start_time_of_the_day).seconds // 3600
            #print("hour diff = ", hour_diff)
            # print(start_time, " hour ", start_time.hour)
            minute_diff = start_time.minute
            date_diff = (start_time.date() - today).days
            # filter date within days_to_display
            if 0 <= date_diff < days_to_display:
                index = date_diff * slots_per_day
                if is_contracted_tutor:
                    index += hour_diff * 2 + minute_diff // 30
                else:
                    index += hour_diff
                #print("date_diff = ", date_diff, "hour_diff = ", hour_diff,
                #        "minute_diff = ", minute_diff, "index = ", index)
                #print(index)
                timetable[index]['status'] = str(session.status)
                timetable[index]['id'] = session.id
        
        for i in range(days_to_display * slots_per_day):
            if i <= now_index:
                timetable[i]['status'] = "PASSED"
        context['timetable'] = timetable
        # print(timetable)
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
        # Get reviews and ratings
        review_list = self.get_object().review_set.all()
        rating_list = []  # Range for UI. Not numeric.
        compensate_list = []  # 5 - rating. Used for UI.
        num_list = []  # Numeric review rating.
        for review in review_list:
            rating_list.append(range(review.rating))
            compensate_list.append(range(5 - review.rating))
            num_list.append(review.rating)
        context['review_rating_list'] = zip(review_list, rating_list,
                                            compensate_list,
                                            num_list)  # Create list of tuples (review, rating, compensate)
        return context


# -----------------------------------------------------------------------------

# ####### Book Session #######

@login_required(login_url='/auth/login/')
def confirm_booking(request, tutor_id):
    """Confirm booking a new session."""
    if request.method == 'POST':
        user = User.objects.get(username=request.session['username'])
        if user.student is None:  # if not a student, display error message and return
            return HttpResponse("You are not a student!")
        student = Student.objects.get(user=user)
        tutor = Tutor.objects.get(pk=tutor_id)
        new_session = Session.objects.get(
            pk=request.POST.get('session_id', ''))
        
        if (tutor.username == student.username):
            # TODO: beautify
            return HttpResponse("You can't book your own session.")

        now = datetime.now()
        time_diff = new_session.start_time - timezone.make_aware(now)
        #print("time_diff = ", time_diff)
        if time_diff <= timedelta(days=1):
            return HttpResponse("You cannot book a session within 24 hours before start_time!")

        # Ignore commission for now because it might be saved by coupon
        if (student.wallet_balance - tutor.hourly_rate) < 0:
            # TODO: beautify
            return HttpResponse("Your balance is " +
                                str(student.wallet_balance) +
                                ". You don't have enough money.")

        if tutor.username == student.username:
            # TODO: beautify
            return HttpResponse("You can't book your session.")
        # Check if student has already booked a session on that day.
        hist_booking_list = student.bookingrecord_set.all()
        for hist_booking in hist_booking_list:
            if hist_booking.session.start_time.date() == \
                    new_session.start_time.date() and \
                            hist_booking.tutor == tutor and hist_booking.status != 'C':
                return HttpResponse("You can only book one session per day!")
        return render(request, 'book.html',
                      {'tutor': tutor,
                       'session': new_session,
                       'balance': student.wallet_balance - tutor.hourly_rate * 1.05,
                       'commission': tutor.hourly_rate * 0.05,
                       'total': tutor.hourly_rate * 1.05})


@login_required(login_url='/auth/login/')
def save_booking(request, tutor_id):
    """Save booking record and redirect to the dashboard."""
    if request.method == 'POST':
        user = User.objects.get(username=request.session['username'])
        student = user.student
        session_id = request.POST.get('session_id', '')
        tutor = Tutor.objects.get(pk=tutor_id)
        session = Session.objects.get(pk=session_id)
        # # TODO: mark session as selected
        # if not session.status == session.BOOKABLE:
        #     # TODO: handle exception
        #     # return
        #     pass
        # added following lines for testing.  - Jiayao
        session.tutor = tutor
        session.status = session.BOOKED
        session.save()
        now = datetime.now()
        if (student.wallet_balance - tutor.hourly_rate * 1.05) < 0:
            return HttpResponse("No enough money!")
        # Create a new transaction and save it.
        transaction = Transaction(issuer=student, receiver=tutor,
                                  amount=tutor.hourly_rate,
                                  created_at=now,
                                  commission=tutor.hourly_rate * 0.05)
        transaction.save()
        # Create a new booking record and save it.
        bookRecord = BookingRecord(
            tutor=tutor, student=student, session=session, entry_date=now,
            transaction=transaction)
        bookRecord.save()
        # Deduct fee (including commission) from student's wallet
        student.wallet_balance -= tutor.hourly_rate * 1.05
        # Send emails to both students and tutors.
        msgToStudent = 'Your booking with ' + tutor.first_name + ' ' + tutor.last_name + ' from ' + \
                       str(session.start_time) + ' to ' + \
                       str(session.end_time) + ' has been confirmed.'
        send_mail('Booking Confirmed', msgToStudent,
                  'noreply@hola-inc.top', [student.email], False)
        msg_to_tutor = 'Your booking with ' + student.first_name + ' ' + student.last_name + ' from ' + \
                       str(session.start_time) + ' to ' + \
                       str(session.end_time) + ' has been confirmed.'
        send_mail('Booking Confirmed', msg_to_tutor,
                  'noreply@hola-inc.top', [tutor.email], False)
        return redirect("/dashboard/mybookings/")
    else:
        return HttpResponse("not a legal POST request!")


# -----------------------------------------------------------------------------

class ReviewView(LoginRequiredMixin, FormView):
    template_name = 'review.html'
    form_class = ReviewForm
    # success_url = '/thanks/'

    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'

    def can_review(self):
        student = User.objects.get(username=self.request.session['username']).student
        tutor = Tutor.objects.get(pk=self.kwargs['tutor_id'])
        finished_booking_list = BookingRecord.objects.filter(tutor=tutor, student=student, status='F')
        print(finished_booking_list)
        review_list = Review.objects.filter(tutor=tutor, student=student)
        print(review_list)
        return len(finished_booking_list) > len(review_list)

    def dispatch(self, request, *args, **kwargs):
        if self.can_review():
            return super(ReviewView, self).dispatch(request, *args, **kwargs)
        return redirect('/')

    def get_context_data(self, **kwargs):
        context = super(ReviewView, self).get_context_data(**kwargs)
        context['tutor'] = Tutor.objects.get(pk=self.kwargs['tutor_id'])
        return context

    def form_valid(self, form):
        review = form.save(commit=False)
        review.student = User.objects.get(username=self.request.session['username']).student
        tutor_id = self.kwargs['tutor_id']
        review.tutor = Tutor.objects.get(pk=tutor_id)
        review.save()
        return HttpResponse("Review submitted! Thank you.")
