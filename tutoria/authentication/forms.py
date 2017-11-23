"""
authentication/forms.py

Models forms for User registration,
authentication.

Created on Oct. 23, 2017
by Jiayao
"""
from django import forms
from account.models import (User, Tutor, Student, Course, SubjectTag)
from django.core.urlresolvers import reverse_lazy
from django.core.validators import RegexValidator

WIDGET_STYLE_CLASS = {}#{'class' : 'form-control' }

class UpdateUserForm(forms.ModelForm):
	"""Models the form for User profile update."""
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'phone', 'email')

class UpdateTutorForm(forms.ModelForm):
	"""Models the form for Tutor profile update."""
	class Meta:
		model = Tutor
		fields = ('bio', 'hourly_rate', 'tags', 'courses', 'visible')

	hourly_rate = forms.IntegerField(
		widget=forms.widgets.TextInput(attrs={'type': 'number',
										'min': 0, 'step': 10}),
        label='Hourly rate (multiple of 10)',
    )

	def __init__(self, *args, **kwargs):
		super(UpdateTutorForm, self).__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)
		if instance is not None and instance.tutor_type == 'CT':
			self.fields.pop('hourly_rate')



class UserForm(forms.ModelForm):
    """Models the form for User registration."""
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
    )

    phone = forms.CharField()
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'phone')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update(WIDGET_STYLE_CLASS)


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
		widget=forms.widgets.TextInput(attrs={'type': 'number',
										'min': 0, 'step': 10}),
        label='Tell us how much your work worth (per hour, multiple of 10).',
    )

    bio = forms.CharField(
        widget=forms.Textarea(),
        label='Share yourself to your prospective students.',
    )



    university = forms.CharField()

    class Meta:
        model = Tutor
        fields = ('bio', 'tutor_type', 'hourly_rate', 'university')
        exclude = ('user', )

