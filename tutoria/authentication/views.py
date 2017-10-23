"""
authentication/views.py

Created on Oct. 23, 2017
by Jiayao
"""
from __future__ import (absolute_import)
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from account.models import (User, Tutor, Student, SubjectTag,
                           Course)
from .forms import (UserForm, TutorForm)


class SignupView(generic.edit.FormView):
    """Models the sign-up form."""
    template_name = 'signup.html'
    form_class = UserForm

