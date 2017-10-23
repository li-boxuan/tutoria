from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic
from .book_session_form import BookForm

from account.models import (User, Tutor)


def detail(request, tutor_id):
    tutor = get_object_or_404(Tutor, id=tutor_id)
    return render(request, 'detail.html', {'tutor': tutor})


class BookView(BookForm):
    template_name = 'book.html'
    form_class = BookForm
    # success_url = '/thanks/'


def send_book_request(request):
    return HttpResponse("Booking request sent!")
