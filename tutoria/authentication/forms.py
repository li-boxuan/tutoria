"""
authentication/forms.py

Models forms for User registration,
authentication.

Created on Oct. 23, 2017
by Jiayao
"""
from django import forms
from account.models import (Tutor, Student, Course, SubjectTag)
from django.core.urlresolvers import reverse_lazy


WIDGET_STYLE_CLASS = {}#{'class' : 'form-control' }


class UserForm(forms.ModelForm):
    """Models the form for User registration."""
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = Student
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update(WIDGET_STYLE_CLASS)


class TutorForm(forms.ModelForm):
    """Models the form for Tutor profile."""
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
    )

    TUTOR_TYPE_CHOICES = (
        ('CT', 'Contracted Tutor'),
        ('PT', 'Private Tutor')
    )

    tutor_type = forms.ChoiceField(
        label='Are you contracted with the university?',
        widget=forms.RadioSelect(),
        choices=TUTOR_TYPE_CHOICES,
    )

    hourly_rate = forms.IntegerField(
        widget=forms.NumberInput(),
        label='Tell us how much your work worth.',
    )

    bio = forms.CharField(
        widget=forms.Textarea(),
        label='Share yourself to your prospective students.',
    )

    class Meta:
        model = Tutor
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'hourly_rate', 'bio', 'tutor_type')

