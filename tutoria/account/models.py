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
from django.core.exceptions import ValidationError

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
    phone_regex = RegexValidator(regex=r'^\d{9,15}$', message="Phone number must be entered in the format: '12345678'. 8 or 11 digits are allowed.")
    phone = models.CharField(
        max_length=11, blank=True)
    @property
    def tutor(self):
        try:
            tutor = getattr(self, 'tutor_profile')
        except:
            tutor = None
        return tutor

    @property
    def student(self):
        try:
            student = getattr(self, 'student_profile')
        except:
            student = None
        return student

def _hourly_rate_validator(val):
    """Validate whether an hourly_rate is a positive multiple of 10."""
    if not (val >= 0 and val % 10 == 0):
        raise ValidationError(
            _('%(value) must be a positive multiple of 10'),
            params={'value': val}
        )

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

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tutor_profile')
    bio = models.TextField(default='')

    university = models.CharField(
        max_length=128, default='The University of Hong Kong')



    hourly_rate = models.PositiveIntegerField(default=0, validators=[_hourly_rate_validator])
    tags = models.ManyToManyField(SubjectTag, default=None)
    courses = models.ManyToManyField(Course, default=None)
    visible = models.BooleanField(default=True)

    @property
    def avgRating(self):
        """Get the average rating of a tutor. Return 0 by default."""
        review_list = self.review_set.all()
        if (not review_list.exists()) or (len(review_list) <= 3):
            return 5  # Give tutor a 5-star rating by default TODO: add to documentation
        rating_list = []
        for review in review_list:
            rating_list.append(review.rating)
        return sum(rating_list) / float(len(rating_list))

    @property
    def phone(self):
        return self.user.phone

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')

    @property
    def phone(self):
        return self.user.phone
    
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
        return self.username
