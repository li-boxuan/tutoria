"""Form-related classes."""

from django import forms
# TODO: from somewhere import session


# TODO change forms.Form to forms.ModelForm once the Meta model is ready
class BookForm(forms.Form):
    """A form for booking sessions."""

    FRUIT_CHOICES = [
        ('orange', 'Oranges'),
        ('cantaloupe', 'Cantaloupes'),
        ('mango', 'Mangoes'),
        ('honeydew', 'Honeydews'),
        ]

    naive = forms.CharField(label='Naive?',
                            widget=forms.RadioSelect(choices=FRUIT_CHOICES))

# TODO: link the Form class with a Session model
    # class Meta:
    #     model = session
    #     fields = ('', '')
