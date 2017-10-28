"""
account/models.py

Created on Oct. 20, 2017
by Jiayao
"""
from __future__ import (absolute_import, print_function)
from django.db import models
import django.contrib.auth.models as auth_models


class SubjectTag(models.Model):
    """Models subject tags."""
    tag = models.CharField(max_length=128)

    def __str__(self):
        return self.tag


class Course(models.Model):
    """Models courses."""
    course_name = models.CharField(max_length=128)
    course_code = models.CharField(max_length=8)

    def __str__(self):
        return self.course_code + " " + self.course_name

class User(auth_models.User):
    wallet_balance = models.PositiveIntegerField(default=0)
    avatar = models.ImageField()

class Tutor(models.Model):
    """Models the tutor."""
    CONTRACTED_TUTOR = 'CT'
    PRIVATE_TUTOR = 'PT'
    TUTOR_TYPE_CHOICES = (
        (CONTRACTED_TUTOR, 'Contracted Tutor'),
        (PRIVATE_TUTOR, 'Private Tutor'),
    )
    wallet_balance = models.PositiveIntegerField(default=0)
    avatar = models.ImageField()
    tutor_type = models.CharField(
        max_length=2,
        choices=TUTOR_TYPE_CHOICES,
        default=CONTRACTED_TUTOR,
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='')
    hourly_rate = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(SubjectTag)
    courses = models.ManyToManyField(Course)
    visible = models.BooleanField(default=True)
    # sessions = models.ManyToManyField('scheduler.session')

    @property
    def username(self):
        return self.user.username

    @property
    def first_name(self):
        return self.user.first_name

    @first_name.setter
    def first_name(self, val):
        self.user.first_name = val
        self.user.save()

    @property
    def last_name(self):
        return self.user.last_name

    @last_name.setter
    def last_name(self, val):
        self.user.last_name = val
        self.user.save()

    @property
    def email(self):
        return self.user.email

    @email.setter
    def email(self, val):
        self.user.email = val
        self.user.save()

    @property
    def password(self):
        return self.user.password

    @password.setter
    def password(self, val):
        self.user.password = val
        self.user.save()

    @property
    def wallet_balance(self):
        return self.user.wallet_balance

    @wallet_balance.setter
    def wallet_balance(self, bal):
        if bal < 0:
            raise ValueError
        else:
            self.user.wallet_balance = bal
            self.user.save()

    @property
    def avatar(self):
        return self.user.avatar

    @avatar.setter
    def avatar(self, avt):
        self.user.avatar = avt
        self.user.save()

    def __str__(self):
        return "{}: {}".format(self.username, self.tutor_type)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def username(self):
        return self.user.username

    @property
    def first_name(self):
        return self.user.first_name

    @first_name.setter
    def first_name(self, val):
        self.user.first_name = val
        self.user.save()

    @property
    def last_name(self):
        return self.user.last_name

    @last_name.setter
    def last_name(self, val):
        self.user.last_name = val
        self.user.save()

    @property
    def email(self):
        return self.user.email

    @email.setter
    def email(self, val):
        self.user.email = val
        self.user.save()

    @property
    def password(self):
        return self.user.password

    @password.setter
    def password(self, val):
        self.user.password = val
        self.user.save()

    @property
    def wallet_balance(self):
        return self.user.wallet_balance

    @wallet_balance.setter
    def wallet_balance(self, bal):
        if bal < 0:
            raise ValueError
        else:
            self.user.wallet_balance = bal
            self.user.save()

    @property
    def avatar(self):
        return self.user.avatar

    @avatar.setter
    def avatar(self, avt):
        self.user.avatar = avt
        self.user.save()



    def __str__(self):
        return self.username

