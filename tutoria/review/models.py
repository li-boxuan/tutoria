"""Models for tutor reviews. -- Jingran."""
from django.db import models
# from django.utils import timezone


class Review(models.Model):
    """Model for tutor reviews."""

    content = models.TextField()  # Content of review
    rating = models.FloatField()  # Rating varies from 0 to 5
    # Which student wrote this review. Many-to-one relation.
    student = models.ForeignKey('account.Student', on_delete=models.CASCADE)
    # Which tutor receives this review. Many-to-one relation.
    tutor = models.ForeignKey('account.Tutor', on_delete=models.CASCADE)
    # When this review's created. Automatically set when obj first created.
    date = models.DateTimeField(auto_now_add=True)
    anonymous = models.BooleanField()  # True if review is anonymous.

    def __str__(self):
        """How a review object is displayed as string."""
        return """To Tutor: {}\nFrom Student: {}\nTime: {}\nAnonymous = {}\n
                  Rating {}/5.0\nContent:\n{}""".format(self.tutor,
                                                        self.student,
                                                        self.date,
                                                        self.anonymous,
                                                        self.rating,
                                                        self.content)
