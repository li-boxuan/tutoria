from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from scheduler.models import BookingRecord



def MybookingsView(request):
    #model = scheduler
    record = student.BookingRecord_set.all
    #template_name = 'my_bookings.html'
    #context_object_name = 'mybookings'
    return render(request, 'my_bookings.html', {'record': record})
