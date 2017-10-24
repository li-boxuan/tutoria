from django import forms


class BookForm(forms.Form):
    FRUIT_CHOICES = [
        ('orange', 'Oranges'),
        ('cantaloupe', 'Cantaloupes'),
        ('mango', 'Mangoes'),
        ('honeydew', 'Honeydews'),
        ]

    naive = forms.CharField(label='Naive?',
                            widget=forms.RadioSelect(choices=FRUIT_CHOICES))
