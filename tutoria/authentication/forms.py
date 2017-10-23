"""
authentication/forms.py

Models forms for User registration,
authentication.

Created on Oct. 23, 2017
by Jiayao
"""
from django import forms
from account.models import (User, Tutor, Student, Course, SubjectTag)


WIDGET_STYLE_CLASS = {'class' : 'form-control' }


class UserForm(forms.ModelForm):
    """Models the form for User registration."""
    SIGNUP_CHOICE = (('S', 'I am a Student'),
                     ('T', 'I am a Tutor'),
                     ('B', 'I can be both =D'),
                    )
    # email = forms.EmailField(
    #     label='Enter your e-mail.',
    #     widget=forms.EmailInput(),
    # )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
    )
    signup_type = forms.ChoiceField(
        label="Are you a student or a tutor?",
        widget=forms.RadioSelect(),
        choices=SIGNUP_CHOICE,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, filed in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += WIDGET_STYLE_CLASS['class']
            else:
                field.widget.attrs.update(WIDGET_STYLE_CLASS)

    class Meta:
        model = User
        fields = ('username', 'password', 'signup_type', 'email', 'first_name', 'last_name')


class TutorForm(forms.ModelForm):
    """Models the form for Tutor profile."""
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
        fields = ('hourly_rate', 'bio', 'tutor_type')
