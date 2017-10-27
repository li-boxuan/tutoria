"""Form-related classes."""

from django import forms
from scheduler.models import Session


# TODO change forms.Form to forms.ModelForm once the Meta model is ready
class BookForm(forms.Form):
    """A form for booking sessions."""

    DATE_CHOICES = [
        ('slot_0', '8:30-9:00'),
        ('slot_1', '9:00-9:30'),
        ('slot_2', '9:30-10:00'),
        ('slot_3', '10:00-10:30'),
        ('slot_4', '10:30-11:30'),
        ('slot_5', '11:30-12:00'),
        ('slot_6', '12:00-12:30'),
        ]

    naive = forms.CharField(label='Select a session...',
                            widget=forms.RadioSelect(choices=DATE_CHOICES))

    class Meta:
        """Meta class holding the Session model."""

        model = Session
        fields = ('start_date', 'start_hour', 'start_minute')
