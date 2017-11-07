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
from django.contrib.auth import (authenticate, login, logout)
from django.contrib.auth.decorators import login_required
from account.models import (User, Tutor, Student, SubjectTag,
                           Course)
from .forms import (UserForm, TutorForm)

class SINGUP_STATUS:
    NONE = 0
    SUCCESS = 1
    EXISTED = 2
    FAILED = 3


class IndexView(generic.TemplateView):
    """Models the index view."""
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['choice'] = True
        context['user_form'] = None
        context['tutor_form'] = None
        context['status'] = SINGUP_STATUS.NONE
        context['SIGNUP_STATUS'] = SINGUP_STATUS
        return context

class LoginView(generic.TemplateView):
    """Models the login view."""
    template_name = 'login.html'


    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['status'] = 1
        return context

    def post(self, req, *args, **kwargs):
        user = authenticate(username=req.POST['username'],
                           password=req.POST['password'])
        if user is not None:
            login(req, user)
            req.session['username'] = req.POST['username']
            if user.is_staff:
                return HttpResponseRedirect(reverse('admin:index'))
            return HttpResponseRedirect(reverse('homepage'))
        else:
            return render(req, self.template_name, {'status': 0})

@login_required
def logout_view(req):
    logout(req)
    req.session['username'] = None
    return HttpResponseRedirect(reverse('homepage'))

class StudentFormView(generic.edit.CreateView):
    """Models the sign-up form."""
    template_name = 'signup.html'
    form_class = UserForm

class TutorFormView(generic.edit.CreateView):
    """Models the sign-up form."""
    template_name = 'signup.html'
    form_class = TutorForm


class StudentView(IndexView):

    def get(self, req, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['choice'] = False
        context['user_form'] = UserForm(prefix='user_form')
        return self.render_to_response(context)

    def post(self, req, *args, **kwargs):
        context = self.get_context_data()
        form = UserForm(req.POST, prefix='user_form')
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)
                context['status'] = SINGUP_STATUS.EXISTED
            except User.DoesNotExist:
                user = form.save()
                user.set_password(password)
                user.save()
                student = Student.objects.create(user=user)
                context['status'] = SINGUP_STATUS.SUCCESS
        else:
            context['status'] = SINGUP_STATUS.FAILED
        return self.render_to_response(context)


class TutorView(IndexView):

    def get(self, req, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['choice'] = False
        context['user_form'] = UserForm(prefix='user_form')
        context['tutor_form'] = TutorForm(prefix='tutor_form')
        return self.render_to_response(context)

    def post(self, req, *args, **kwargs):
        context = self.get_context_data()
        form = UserForm(req.POST, prefix='user_form')
        tutor_form = TutorForm(req.POST, prefix='tutor_form')
        if form.is_valid() and tutor_form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)
                context['status'] = SINGUP_STATUS.EXISTED
            except User.DoesNotExist:
                user = form.save()
                user.set_password(password)
                user.save()
                tutor_form.cleaned_data['user'] = user
                tutor = tutor_form.save(commit=False)
                tutor.user = user
                tutor.save()
                context['status'] = SINGUP_STATUS.SUCCESS
        else:
            context['status'] = SINGUP_STATUS.FAILED
        return self.render_to_response(context)


class BothView(IndexView):
    """Models the sign-up form."""

    def get(self, req, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['choice'] = False
        context['user_form'] = UserForm(prefix='user_form')
        context['tutor_form'] = TutorForm(prefix='tutor_form')
        return self.render_to_response(context)

    def post(self, req, *args, **kwargs):
        context = self.get_context_data()
        form = UserForm(req.POST, prefix='user_form')
        tutor_form = TutorForm(req.POST, prefix='tutor_form')
        if form.is_valid() and tutor_form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)
                context['status'] = SINGUP_STATUS.EXISTED
            except User.DoesNotExist:
                user = form.save()
                user.set_password(password)
                user.save()
                tutor_form.cleaned_data['user'] = user
                tutor = tutor_form.save(commit=False)
                tutor.user = user
                tutor.save()
                student = Student.objects.create(user=user)
                context['status'] = SINGUP_STATUS.SUCCESS
        else:
            context['status'] = SINGUP_STATUS.FAILED
        return self.render_to_response(context)
