"""Dashborad views."""
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from wallet.models import Transaction
from scheduler.models import BookingRecord, Session
from account.models import User, Student, Tutor
from django.contrib.auth.decorators import login_required

from datetime import datetime, timedelta
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
                if context['record'].student == stu:
                    context['selected_type'] = 'as_stu'
                else:
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

class MyTimetableView(generic.ListView):
    model = BookingRecord
    template_name = 'my_timetable.html'
    context_object_name = 'my_booking_records'

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
        amount = int(req.POST['amount'])
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
        






