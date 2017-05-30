# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.core.files.storage import FileSystemStorage



class Profile(models.Model):
    user = models.OneToOneField(User)
    DOB = models.DateField()
    college = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.user.first_name


class UserType(models.Model):
    name = models.CharField(max_length=75)
    user = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name


class Certificate(models.Model):
    abc = FileSystemStorage()
    template = models.FileField(upload_to='a',blank=True,null=True)
    logo = models.CharField(max_length=25)

    def __str__(self):
        return self.logo


class Event(models.Model):
    name = models.CharField(max_length=100)
    certificate = models.OneToOneField(Certificate, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.name


class OrganisedEvent(models.Model):
    event = models.ForeignKey(Event)
    start_date = models.DateField()
    end_date = models.DateField()
    num_of_days = models.IntegerField()
    participant = models.ManyToManyField(User, related_name='user', through='UserCertificateInfo', blank=True)

    def __str__(self):
        return self.event.name


class UserCertificateInfo(models.Model):
    user = models.ForeignKey(User, default='admin')
    organise_event = models.ForeignKey(OrganisedEvent)
    days_attended = models.IntegerField()
    qrcode = models.IntegerField()

    def __str__(self):
        return self.user.first_name


