"""Dashborad views."""
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from wallet.models import Transaction
from scheduler.models import BookingRecord, Session
from account.models import User, Student, Tutor
from django.contrib.auth.decorators import login_required

from datetime import datetime, timedelta, date, time
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
           context['username'] = self.request.session['username']
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
           context['records'] = []
           for r in records:
               one_month_before_now = timezone.now() - timedelta(days=30)
               if r.entry_date > one_month_before_now:
                   context['records'].append(r)
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
                stu = Student.objects.get(user=user)
                context['is_student'] = 'true'
            except Student.DoesNotExist:
                context['is_student'] = 'false'
            try:
                tut = Tutor.objects.get(user=user)
                context['is_tutor'] = 'true'
            except Tutor.DoesNotExist:
                context['is_tutor'] = 'false'
            if 'id' in self.request.GET:
                context['id'] = 'selected'
                context['record'] =BookingRecord.objects.filter(id=self.request.GET['id']).first()
                if context['is_student'] == 'true':
                    if context['record'].student == stu:
                        context['selected_type'] = 'as_stu'
                if context['is_tutor'] == 'true':
                    if context['record'].tutor == tut:
                        context['selected_type'] = 'as_tut'
                return context
            else:
                context['id'] = 'not_selected'
                if context['is_tutor'] == 'true':
                    context['records_as_tut'] = tut.bookingrecord_set.all()
                if context['is_student'] == 'true':
                    context['records_as_stu'] = stu.bookingrecord_set.all()
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
            refund = bkrc.transaction.amount + bkrc.transaction.commission
            usrn = self.request.session['username']
            user = User.objects.get(username=usrn)
            usr = get_object_or_404(Student, user=user)
            usr.wallet_balance += refund
            usr.save()
            bkrc.status = BookingRecord.CANCELED
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
        isStudent = False
        isTutor = False

        if self.request.session['username'] is None:
            context['timetable'] = None
            return context
        else:
            usrn = self.request.session['username']
            user = User.objects.get(username=usrn)
        
        try:
            usr = Tutor.objects.get(user=user)
            isTutor = True
        except Tutor.DoesNotExist:
            pass

        context['is_tutor'] = isTutor
        if isTutor:
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
            now = datetime.now()
            if is_contracted_tutor:
                now_index = now.hour * 2 + now.minute // 30
            else:
                now_index = now.hour

            for i in range(days_to_display * slots_per_day):
                # add all timeslots that are not in database as CLOSED session
                # TODO this part might be dirty, we should create all sessions in advance
                d = today + timedelta(days = i // slots_per_day)
                if is_contracted_tutor:
                    hour = (i % slots_per_day) // 2
                    minute = 0 if hour % 2 == 0 else 30
                else:
                    hour = i % slots_per_day
                    minute = 0
                start_time = datetime.combine(d, time(hour, minute))
                if is_contracted_tutor:
                    end_time = start_time + timedelta(minutes = 30)
                else:
                    end_time = start_time + timedelta(hours = 1)
                session, _ = Session.objects.get_or_create(
                    start_time=timezone.make_aware(start_time),
                    end_time=timezone.make_aware(end_time),
                    tutor=usr)
                elem = {'status' : session.status, 'date' : str(today + timedelta(days=i // slots_per_day)), 'id': session.id}
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
                    if session.status == session.BOOKED:
                        # logic is a bit tricky here
                        # note we won't pass session id but booking_record id here
                        # because one session can have multiple booking records
                        # tutor wants to see the latest record when clicking the slot
                        records = session.bookingrecord_set.all()
                        for record in records:
                            if record.status == record.INCOMING:
                                timetable[index]['id'] = record.id
                                break
            for i in range(days_to_display * slots_per_day):
                if i <= now_index:
                    timetable[i]['status'] = "PASSED"

            context['tutor_timetable'] = timetable
            #print(timetable)

        try:
            usr = Student.objects.get(user=user)
            isStudent = True
        except Student.DoesNotExist:
            pass

        context['is_student'] = isStudent
        if isStudent:
            context['student'] = usr
            # generate a 1D array which stores the timetable
            # there are 14 days
            slots_per_day = 48
            days_to_display = 7
            timetable = []
            # retrieve date of today
            today = date.today()
            now = datetime.now()
            now_index = now.hour * 2 + now.minute // 30
            for i in range(days_to_display * slots_per_day):
                elem = {'status' : 'X', 'date' : str(today + timedelta(days=i // slots_per_day)), 'id': ''}
                timetable.append(elem) # closed

            for record in usr.bookingrecord_set.all():
                start_time = record.session.start_time
                hour_diff = start_time.hour - 0 # if timetable starts from 0
                hour_diff += 8 # timezone issue (todo)
                #print(start_time, " hour ", start_time.hour)
                minute_diff = start_time.minute
                date_diff = (start_time.date() - today).days
                # filter date within days_to_display
                if 0 <= date_diff < days_to_display:
                    index = date_diff * slots_per_day
                    index += hour_diff * 2 + minute_diff // 30
                    # print("date_diff = ", date_diff, "hour_diff = ", hour_diff,
                    #        "minute_diff = ", minute_diff, "index = ", index)
                    #print(index)
                    if record.status == record.INCOMING or record.status == record.ONGOING:
                        # TODO what about other states?
                        timetable[index]['status'] = 'A' # use 'A' to represent this record has detail to be referred
                        timetable[index]['id'] = record.id
                        if record.tutor.tutor_type == record.tutor.PRIVATE_TUTOR:
                            timetable[index + 1]['status'] = 'A'
                            timetable[index + 1]['id'] = record.id

            for i in range(days_to_display * slots_per_day):
                if i <= now_index:
                    timetable[i]['status'] = "PASSED"
            context['student_timetable'] = timetable
            #print(timetable)

        return context

    def post(self, request, **kwargs):
        # TODO past time cannot be modified
        session_id = self.request.POST.get('session_id', '')
        session = Session.objects.get(id=session_id)
        #print("before update, session = ", session, " status = ", session.status)
        if session.status == session.CLOSED:
            session.status = session.BOOKABLE
        elif session.status == session.BOOKABLE:
            session.status = session.CLOSED
        session.save()
        #print("after update, session = ", session, " status = ", session.status)
        return redirect('/dashboard/mytimetable/')


class MyWalletView(generic.TemplateView):
    template_name = 'my_wallet.html'
        
    def get_context_data(self, **kwargs):
        context = super(MyWalletView, self).get_context_data(**kwargs)
        if self.request.session['username'] is None:
           return context
        else:
           context['status'] = 1
           usrn = self.request.session['username']
           user = User.objects.get(username=usrn)
           context['balance'] = user.wallet_balance
           return context

    def post(self, req, *args, **kwargs):
        usrn = self.request.session['username']
        user = User.objects.get(username=usrn)
        balance = user.wallet_balance
        op = req.POST['operation']
        amount = float(req.POST['amount'])
        print(op)
        if op == 'topup':
            user.wallet_balance += amount;
            user.save()
            return render(req, self.template_name, {'status': 2, 'balance': user.wallet_balance})
        else:
            if amount > balance:
                return render(req, self.template_name, {'status': 0, 'balance': user.wallet_balance})
            else:
                user.wallet_balance -= amount;
                user.save()
                return render(req, self.template_name, {'status': 2, 'balance': user.wallet_balance})
