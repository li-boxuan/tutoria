"""Dashborad views."""
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from wallet.models import Transaction
from scheduler.models import BookingRecord, Session
from account.models import User, Student, Tutor
from django.contrib.auth.decorators import login_required

from datetime import datetime, timedelta, date
from django.utils import timezone
from django.core.mail import send_mail

# def MybookingsView(request):
#    #model = scheduler
#    record = student.BookingRecord_set.all
#    #template_name = 'my_bookings.html'
#    #context_object_name = 'mybookings'
#    return render(request, 'my_bookings.html', {'record': record})

class MytransactionsView(generic.ListView):
    model = Transaction
    template_name = 'my_transactions.html'
    context_object_name = 'my_transaction_records'

    def get_context_data(self, **kwargs):
        context = super(MytransactionsView, self).get_context_data(**kwargs)
        #print datetime.now()
        if self.request.session['username'] is None:
           context['records'] = None
           return context
        else:
           usrn = self.request.session['username']
           user = User.objects.get(username=usrn)
           try:
               usr = Student.objects.get(user=user)
               context['user_type'] = 'Student' 
           except Student.DoesNotExist:
               usr = Tutor.objects.get(user=user)
               context['user_type'] = 'Tutor' 
#usr = get_object_or_404(Student, user=user)
           records = usr.bookingrecord_set.all()
           context['records'] = records
           transactions = []
           for rec in context['records']:
               transactions.append(rec.transaction)
           context['transactions'] = transactions
           context['zipped'] = zip(records,transactions)
           context['balance'] = usr.wallet_balance
           return context


    



class MybookingsView(generic.ListView):
    model = BookingRecord
    template_name = 'my_bookings.html'
    context_object_name = 'my_booking_records'

    def get_context_data(self, **kwargs):
        context = super(MybookingsView, self).get_context_data(**kwargs)

        if self.request.session['username'] is None:
            context['records'] = None
            return context
        else:
            usrn = self.request.session['username']
            user = User.objects.get(username=usrn)
            try:
                usr = Student.objects.get(user=user)
                context['user_type'] = 'Student'
            except Student.DoesNotExist:
                usr = Tutor.objects.get(user=user)
                context['user_type'] = 'Tutor'
#usr = get_object_or_404(Student, user=user)
            if 'id' in self.request.GET:
                context['id'] = 'selected'
                context['records'] =BookingRecord.objects.filter(id=self.request.GET['id'])
                return context
            else:
                context['id'] = 'not_selected'
                context['records'] = usr.bookingrecord_set.all()
                #print usr.wallet_balance
                return context

    def post(self, request, **kwargs):
        print(request)
        bkRecord_id = self.request.POST.get('booking_id', '')
        bkrc = BookingRecord.objects.filter(id=bkRecord_id).first()
        sess = Session.objects.get(bookingrecord=bkrc)
        one_day_from_now = timezone.now() + timedelta(hours=24)
        if one_day_from_now < sess.start_time:
            sess.status = Session.BOOKABLE
            sess.save()  # save is needed for functioning  - Jiayao
            refund = bkrc.transaction.amount
            usrn = self.request.session['username']
            user = User.objects.get(username=usrn)
            usr = get_object_or_404(Student, user=user)
            #print usr.wallet_balance
            usr.wallet_balance += refund
            usr.save()
            #print "refund!" + str(refund)
            #print usr.wallet_balance
            bkrc.status = BookingRecord.CANCELED
            #print bkrc.status
            bkrc.save()
            tut = bkrc.tutor
            send_mail('Session Canceled', 'Please check on Tutoria, your session with '+ bkrc.tutor.first_name + ' ' + bkrc.tutor.last_name +  ' from ' + str(sess.start_time) + ' to ' + str(sess.end_time) +  ' has been canceled.', 'nonereplay@hola-inc.top', [usr.email], False)
            send_mail('Session Canceled', 'Please check on Tutoria, your session with '+ bkrc.student.first_name + ' ' + bkrc.student.last_name +  ' from ' + str(sess.start_time) + ' to ' + str(sess.end_time) +  ' has been canceled.', 'nonereplay@hola-inc.top', [tut.email], False)
            return redirect('dashboard/mybookings/')
        else:
            return HttpResponse("This session is within 24 hours and can't be canceled!")

class MytimetableView(generic.ListView):
    model = BookingRecord
    template_name = 'my_timetable.html'
    context_object_name = 'my_timetable'

    def get_context_data(self, **kwargs):
        """Get context data."""
        context = super(MytimetableView, self).get_context_data(**kwargs)

        if self.request.session['username'] is None:
            context['timetable'] = None
            return context
        else:
            usrn = self.request.session['username']
            user = User.objects.get(username=usrn)
            try:
                usr = Student.objects.get(user=user)
                context['user_type'] = 'Student'
            except Student.DoesNotExist:
                usr = Tutor.objects.get(user=user)
                context['user_type'] = 'Tutor'

        # (todo:bxli) Assume usr is a teacher here
        context['tutor'] = usr
        # generate a 1D array which stores the timetable
        # there are 14 days
        # private tutor has 24 timeslots per day while contracted tutor has 48
        is_contracted_tutor = usr.tutor_type == 'CT'
        slots_per_day = 48 if is_contracted_tutor else 24
        days_to_display = 14
        timetable = []
        # retrieve date of today
        today = date.today()
        for i in range(days_to_display * slots_per_day):
            elem = {'status' : 'X', 'date' : str(today + timedelta(days=i / slots_per_day)), 'id': ''}
            #print(elem)
            timetable.append(elem) # closed
        # print("tot: " + str(days_to_display * slots_per_day))
        # convert "date" of today to "datetime" of today's 0 'o clock
        # init_time = datetime.combine(today, datetime.min.time())
        for session in usr.session_set.all():
            start_time = session.start_time
            hour_diff = start_time.hour - 0 # if timetable starts from 0
            hour_diff += 8 # timezone issue (todo)
            #print(start_time, " hour ", start_time.hour)
            minute_diff = start_time.minute
            date_diff = (start_time.date() - today).days
            # filter date within days_to_display
            if 0 <= date_diff < days_to_display:
                index = date_diff * slots_per_day
                if is_contracted_tutor:
                    index += hour_diff * 2 + minute_diff // 30
                else:
                    index += hour_diff
                # print("date_diff = ", date_diff, "hour_diff = ", hour_diff,
                #        "minute_diff = ", minute_diff, "index = ", index)
                #print(index)
                timetable[index]['status'] = str(session.status)
                timetable[index]['id'] = session.id
        context['timetable'] = timetable
        # print(timetable)
        return context

