from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from account.models import (User, Tutor)

def detail(request, tutor_id):
    tutor = get_object_or_404(Tutor, id=tutor_id)
    return render(request, 'detail.html', {'tutor': tutor})

