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

class Tutor(auth_models.User):
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

    bio = models.TextField(default='')
    hourly_rate = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(SubjectTag)
    courses = models.ManyToManyField(Course)
    visible = models.BooleanField(default=True)
    # sessions = models.ManyToManyField('scheduler.session')

    def __str__(self):
        return "{}: {}".format(self.username, self.tutor_type)


class Student(auth_models.User):
    def __str__(self):
        return self.username
    wallet_balance = models.PositiveIntegerField(default=0)
    avatar = models.ImageField()

