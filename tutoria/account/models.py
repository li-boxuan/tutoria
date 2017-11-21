"""
account/models.py

Created on Oct. 20, 2017
by Jiayao
"""
from __future__ import (absolute_import, print_function)
from django.db import models
import django.contrib.auth.models as auth_models
import os
from django.core.validators import RegexValidator


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
    avatar = models.ImageField(default='default_avatar.png')


class Tutor(models.Model):
    """Models the tutor."""
    CONTRACTED_TUTOR = 'CT'
    PRIVATE_TUTOR = 'PT'
    TUTOR_TYPE_CHOICES = (
        (CONTRACTED_TUTOR, 'Contracted Tutor'),
        (PRIVATE_TUTOR, 'Private Tutor'),
    )
    tutor_type = models.CharField(
        max_length=2,
        choices=TUTOR_TYPE_CHOICES,
        default=CONTRACTED_TUTOR,
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+85212345678' or '12345678'. 8 or 11 digits are allowed.")
    phone = models.CharField(
        validators=[phone_regex], max_length=11, blank=True)
    university = models.CharField(
        max_length=128, default='The University of Hong Kong')
    hourly_rate = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(SubjectTag, default=None)
    courses = models.ManyToManyField(Course, default=None)
    visible = models.BooleanField(default=True)
    # sessions = models.ManyToManyField('scheduler.session')

    @property
    def avgRating(self):
        """Get the average rating of a tutor. Return 0 by default."""
        # TODO: don't display untill more than 3 reviews received.
        review_list = self.review_set.all()
        if not review_list.exists():
            return 0
        rating_list = []
        for review in review_list:
            rating_list.append(review.rating)
        return sum(rating_list) / float(len(rating_list))

    @property
    def full_name(self):
        return self.user.first_name + " " + self.user.last_name

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
