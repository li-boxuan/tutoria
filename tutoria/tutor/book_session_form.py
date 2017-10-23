from django import forms


class BookForm(forms.Form):
    FRUIT_CHOICES = [
        ('orange', 'Oranges'),
        ('cantaloupe', 'Cantaloupes'),
        ('mango', 'Mangoes'),
        ('honeydew', 'Honeydews'),
        ]

    naiveField = forms.CharField(label='Naive?', choices=FRUIT_CHOICES,
                                 widget=forms.RadioSelect())
