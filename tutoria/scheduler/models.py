"""
scheduler/models.py

Created on Oct. 20, 2017
by Jiayao
"""
from __future__ import (absolute_import, print_function)
from django.db import models


class Session(models.Model):
    '""Models the session.""'
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

    def __str__(self):
        return '{} -- {}\nTutor: {} ({})'.format(self.start_time, self.end_time,
                                                 self.tutor, self.status)


class BookingRecord(models.Model):
    '""Models booking record.""'
    # TODO: update on_deletion methods to SET()
    INCOMING = 'I'
    CANCELED = 'C'
    FINISHED = 'F'
    ONGOING = 'O'
    STATUS_CHOICES = (
        (INCOMING, 'In-coming'),
        (CANCELED, 'Canceled'),
        (FINISHED, 'Finished'),
        (ONGOING, 'On-going')
    )
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=INCOMING)
    tutor = models.ForeignKey('account.Tutor', on_delete=models.CASCADE)
    student = models.ForeignKey('account.Student', on_delete=models.CASCADE)
    session = models.ForeignKey('scheduler.Session', on_delete=models.CASCADE)
    entry_date = models.DateTimeField()
    transaction = models.ForeignKey(
        'wallet.Transaction', on_delete=models.CASCADE)

    def __str__(self):
        # Ignore PycodestyleBear (E501)
        return 'Tutor: {}\nStudent: {}\n Session\n{}'.format(self.tutor, self.student, self.session)
