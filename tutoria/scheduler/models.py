"""
scheduler/models.py

Created on Oct. 20, 2017
by Jiayao
"""
from __future__ import (absolute_import, print_function)
from django.db import models


class Session(models.Model):
    """Models the session."""
    BOOKABLE = 'A'
    BOOKED = 'B'
    CLOSED = 'X'
    STATUS_CHOICES = (
        (CLOSED, 'Closed'),
        (BOOKED, 'Booked'),
		(BOOKABLE, 'BOOKABLE'),
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    tutor = models.ForeignKey('account.Tutor', on_delete=models.CASCADE)
    status = models.CharField(max_length=1,
                              choices=STATUS_CHOICES,
                              default=CLOSED,
                              )


class BookingRecord(models.Model):
    """Models booking record."""
    # TODO: update on_deletion methods to SET()
    tutor = models.ForeignKey('account.Tutor', on_delete=models.CASCADE)
    student = models.ForeignKey('account.Student', on_delete=models.CASCADE)
    session = models.ForeignKey('scheduler.Session', on_delete=models.CASCADE)
    entry_date = models.DateTimeField()
    transaction = models.ForeignKey('wallet.Transaction', on_delete=models.CASCADE)

