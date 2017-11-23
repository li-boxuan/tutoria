from django import forms
from review.models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        exclude = ['student', 'tutor', 'date']
