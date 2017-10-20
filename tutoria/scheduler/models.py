"""
scheduler/models.py

Created on Oct. 20, 2017
by Jiayao
"""
from __future__ import (absolute_import, print_function)
from django.db import models


class Session(models.Model):
    """Models the session."""
    OPEN = 'O'
    CLOSED = 'X'
    STATUS_CHOICES = (
        (CLOSED, 'Closed'),
        (OPEN, 'Open'),
    )
    start_date = models.DateField()
    start_hour = models.PositiveSmallIntegerField()
    start_minute = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=1,
                              choices=STATUS_CHOICES,
                              default=OPEN,
                              )


class BookingRecord(models.Model):
    """Models booking record."""
    # TODO: update on_deletion methods to SET()
    tutor = models.ForeignKey('account.Tutor', on_delete=models.CASCADE)
    student = models.ForeignKey('account.Student', on_delete=models.CASCADE)
    session = models.ForeignKey('scheduler.Session', on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    transaction = models.ForeignKey('wallet.Transaction', on_delete=models.CASCADE)

