"""Dashborad views."""
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from scheduler.models import BookingRecord, Session
from account.models import User, Student
from django.contrib.auth.decorators import login_required


# def MybookingsView(request):
#    #model = scheduler
#    record = student.BookingRecord_set.all
#    #template_name = 'my_bookings.html'
#    #context_object_name = 'mybookings'
#    return render(request, 'my_bookings.html', {'record': record})

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
            ursn = self.request.session['username']
            user = User.objects.get(username=ursn)
            urs = get_object_or_404(Student, user=user)
            context['records'] = urs.bookingrecord_set.all()
            # context= BookingRecord.objects.filter(student.username==ursn)
            return context

    def post(self, request, **kwargs):
        print(request)
        bkRecord_id = self.request.POST.get('booking_id', '')
        bkrc = BookingRecord.objects.filter(id=bkRecord_id).first()
        # bkrc.session_set.all().status=Session.BOOKABLE
        sess = Session.objects.get(bookingrecord=bkrc)
        sess.status = Session.BOOKABLE
        sess.save()  # save is needed for functioning  - Jiayao

        BookingRecord.objects.filter(id=bkRecord_id).delete()
        return render(request, 'my_bookings.html')
