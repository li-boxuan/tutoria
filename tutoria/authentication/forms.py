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

WIDGET_STYLE_CLASS = {} #{'class' : 'form-control' }

class UpdateUserForm(forms.ModelForm):
	"""Models the form for User profile update."""
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'phone', 'email')

class UpdateTutorForm(forms.ModelForm):
	"""Models the form for Tutor profile update."""
	class Meta:
		model = Tutor
		fields = ('bio', 'hourly_rate', 'tags', 'courses', 'visible', 'tutor_type')

	hourly_rate = forms.IntegerField(
		widget=forms.widgets.TextInput(attrs={'type': 'number',
										'min': 0, 'step': 10,
										'onkeydown': 'return false'}),
        label='Hourly rate (multiple of 10)',
    )

	def __init__(self, *args, **kwargs):
		super(UpdateTutorForm, self).__init__(*args, **kwargs)
		self.fields['tags'].label = 'Tag subjects you can tutor (hold Command or Control for multiple selection):'
		self.fields['courses'].label = 'Tag courses you can tutor (hold Command or Control key for multiples selection):'
		self.fields['visible'].label = 'Make me visible to prospective students.'
		instance = getattr(self, 'instance', None)
		self.fields['tutor_type'].widget.attrs['disabled'] = 'disabled'
		if instance is not None and instance.tutor_type == 'CT':
			self.fields.pop('hourly_rate')



class UserForm(forms.ModelForm):
    """Models the form for User registration."""
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
    )

    #phone = forms.CharField(required=True)
    #phone = forms.RegexField(regex=r'^\+?\d{8,11}$', error_messages={
    #    'invalid': ("Phone number must be entered in the format: '+85261231234' or '61231234'."),
    #    'required': ("Please enter your phone number in either '61231234' or '+85261231234'."),
    #})

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'phone')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['phone'].required = True
        for _, field in self.fields.items():
            field.widget.attrs.update(WIDGET_STYLE_CLASS)


class TutorForm(forms.ModelForm):
    """Models the form for Tutor profile."""

    TUTOR_TYPE_CHOICES = (
        ('CT', 'Contracted Tutor'),
        ('PT', 'Private Tutor')
    )

    UNIVERSITY_CHOICES = (
        ('HKU', 'University of Hong Kong'),
        ('Other', 'Other University')
    )

    tutor_type = forms.ChoiceField(
        label='Are you contracted with the university?',
        widget=forms.RadioSelect(),
        choices=TUTOR_TYPE_CHOICES,
        initial='CT',
    )

    hourly_rate = forms.IntegerField(
		widget=forms.widgets.TextInput(attrs={'type': 'number',
										'min': 0, 'step': 10,
										'onkeydown': 'return false'}),
        label='Tell us how much your work worth (per hour, multiple of 10).',
		initial=0
    )

    bio = forms.CharField(
        widget=forms.Textarea(),
        label='Share yourself to your prospective students.',
    )

    university = forms.ChoiceField(
        label='Unverisity',
        choices=UNIVERSITY_CHOICES,
    )

    visible = forms.BooleanField(
        label='Make my profile visible for prospective students.',
		initial=True
    )

    class Meta:
        model = Tutor
        fields = ('bio', 'tutor_type', 'hourly_rate', 'university', 'visible')
        exclude = ('user', )

    def __init__(self, *args, **kwargs):
        super(TutorForm, self).__init__(*args, **kwargs)
        self.fields['tutor_type'].required = True
        self.fields['university'].required = True
        self.fields['visible'].required = True
        for _, field in self.fields.items():
            field.widget.attrs.update(WIDGET_STYLE_CLASS)
