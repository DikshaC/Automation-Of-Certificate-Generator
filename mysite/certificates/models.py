# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.core.files.storage import FileSystemStorage


class Profile(models.Model):
    user = models.OneToOneField(User)
    DOB = models.DateField()
    college = models.CharField(max_length=300)

    def __str__(self):
        return self.user.first_name


class UserType(models.Model):
    name = models.CharField(max_length=75)
    user = models.ManyToManyField(User, null=True, blank=True)

    def __str__(self):
        return self.name


class Certificate(models.Model):
    abc = FileSystemStorage()
    template = models.FileField(upload_to='media', storage=abc, null=True)

    def __str__(self):
        event = Event.objects.get(certificate=self)
        return event.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    certificate = models.OneToOneField(Certificate, on_delete=models.CASCADE, primary_key=True)
    creator = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class OrganisedEvent(models.Model):
    event = models.ForeignKey(Event)
    start_date = models.DateField()
    end_date = models.DateField()
    num_of_days = models.IntegerField()
    participants = models.ManyToManyField(User, blank=True)
    organiser = models.CharField(max_length=100)
    place = models.CharField(max_length=100)

    def __str__(self):
        return self.event.name


class UserCertificateInfo(models.Model):
    user = models.ForeignKey(User)
    organise_event = models.ForeignKey(OrganisedEvent)
    days_attended = models.IntegerField()
    qrcode = models.IntegerField()

    def __str__(self):
        return self.user.first_name

