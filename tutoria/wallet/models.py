"""
wallet/models.py

Created on Oct. 20, 2017
by Jiayao
"""
from __future__ import absolute_import
from django.db import models


class Transaction(models.Model):
    '""Models a transaction.""'
    issuer = models.ForeignKey('account.Student', on_delete=models.CASCADE,
                               related_name='issuer')
    receiver = models.ForeignKey('account.Tutor', on_delete=models.CASCADE,
                                 related_name='receiver')
    amount = models.FloatField()
    created_at = models.DateTimeField()
    commission = models.FloatField()

    def __str__(self):
        return '{} -> {} :: ${}'.format(self.issuer, self.receiver, self.amount)


class Coupon(models.Model):
    '""Models a coupon.""'
    import uuid
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    code = models.UUIDField(primary_key=True,
                            default=uuid.uuid4, editable=False)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True)
