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
    """Models the user."""
    # username = models.CharField(max_length=128, unique=True)
    # email = models.EmailField(max_length=128, unique=True)
    # first_name = models.CharField(max_length=64, unique=False)
    # last_name = models.CharField(max_length=64, unique=False)
    wallet_balance = models.PositiveIntegerField(default=0)
    avator = models.ImageField()


class Tutor(models.Model):
    """Models the tutor."""
    CONTRACTED_TUTOR = 'CT'
    PRIVATE_TUTOR = 'PT'
    TUTOR_TYPE_CHOICES = (
        (CONTRACTED_TUTOR, 'Contracted Tutor'),
        (PRIVATE_TUTOR, 'Private Tutor'),
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    tutor_type = models.CharField(
        max_length=2,
        choices=TUTOR_TYPE_CHOICES,
        default=CONTRACTED_TUTOR,
    )

    bio = models.TextField(default='')
    hourly_rate = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(SubjectTag)
    courses = models.ManyToManyField(Course)
    sessions = models.ManyToManyField('scheduler.session')

    def __str__(self):
        return "{}: {}".format(self.user.username, self.tutor_type)


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.username


