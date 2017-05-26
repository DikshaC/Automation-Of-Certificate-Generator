# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from datetime import date, datetime
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=75)
    email = models.CharField(max_length=75)
    DOB = models.DateField()
    college = models.CharField(max_length=300, blank=True)


class UserType(models.Model):
    name = models.CharField(max_length=75)
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Certificate(models.Model):
    latex_template = models.CharField(max_length=100)
    logo = models.CharField(max_length=25)

    def __str__(self):
        return self.latex_template


class Event(models.Model):
    name = models.CharField(max_length=100)
    certificate = models.OneToOneField(Certificate, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.name


class OrganisedEvent(models.Model):
    program = models.ForeignKey(Event)
    start_date = models.DateField()
    end_date = models.DateField()
    num_of_days = models.IntegerField()
    user = models.ManyToManyField(User, related_name='user', through='UserCertificateInfo')

    def __str__(self):
        return self.program.name


class UserCertificateInfo(models.Model):
    user = models.ForeignKey(User, default='admin')
    organise_program = models.ForeignKey(OrganisedEvent)
    days_attended = models.IntegerField()
    qrcode = models.IntegerField()

    def __str__(self):
        return self.user.first_name
