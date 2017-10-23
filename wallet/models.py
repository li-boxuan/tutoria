"""
wallet/models.py

Created on Oct. 20, 2017
by Jiayao
"""
from __future__ import absolute_import
from django.db import models


class Transaction(models.Model):
    """Models a transaction."""
    issuer = models.ForeignKey('account.User', on_delete=models.CASCADE,
                              related_name='issuer')
    receiver = models.ForeignKey('account.User', on_delete=models.CASCADE,
                                related_name='receiver')
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField()

    def __str__(self):
        return "{} -> {} :: ${}".format(issuer, receiver, amount)


class Coupon(models.Model):
    """Models a coupon."""
    import uuid
    code = models.UUIDField(primary_key=True,
                           default=uuid.uuid4, editable=False)
    record = models.ForeignKey('scheduler.BookingRecord')

