# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
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
    template = models.FileField( storage=abc, null=True)
    title = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title


class Event(models.Model):
    name = models.CharField(max_length=100)
    certificate = models.OneToOneField(Certificate, on_delete=models.CASCADE, primary_key=True)
    creator = models.ForeignKey(User, related_name="creator")

    def __str__(self):
        return self.name


class OrganisedEvent(models.Model):
    event = models.ForeignKey(Event)
    start_date = models.DateField()
    end_date = models.DateField()
    num_of_days = models.IntegerField()
    participants = models.ManyToManyField(User, blank=True, related_name="participants")
    organiser = models.ForeignKey(User, related_name="organiser")
    place = models.CharField(max_length=100)

    def __str__(self):
        return self.event.name


class UserCertificateInfo(models.Model):
    user = models.ForeignKey(User)
    organise_event = models.ForeignKey(OrganisedEvent)
    duration = models.IntegerField(blank=True, default=0)
    qrcode = models.CharField(max_length=10,default=0)

    def __str__(self):
        return self.user.first_name

