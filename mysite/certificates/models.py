from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.files.storage import FileSystemStorage


class Profile(models.Model):
    user = models.OneToOneField(User)
    dob = models.DateField()
    college = models.CharField(max_length=300)

    def __str__(self):
        return self.user.first_name

    def get_dob(self):
        return self.dob

    def get_college(self):
        return self.college


class UserType(models.Model):
    name = models.CharField(max_length=75)

    def __str__(self):
        return self.name


class Certificate(models.Model):
    abc = FileSystemStorage()
    template = models.FileField(storage=abc, blank=True)
    title = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

    def get_title(self):
        return self.title


class Event(models.Model):
    name = models.CharField(max_length=100)
    certificate = models.OneToOneField(Certificate, on_delete=models.CASCADE, primary_key=True)
    creator = models.ForeignKey(User, related_name="creator")

    def __str__(self):
        return self.name

    def get_certificate(self):
        return self.certificate.title

    def get_creator(self):
        return self.creator.first_name


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

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_num_days(self):
        return self.num_of_days

    def get_participants(self):
        participants = self.participants.all()
        users=[]
        for participant in participants:
            users.append(participant.first_name)

        return users

    def get_organiser(self):
        return self.organiser.first_name

    def get_place(self):
        return self.place


class UserCertificateInfo(models.Model):
    user = models.ForeignKey(User)
    organised_event = models.ForeignKey(OrganisedEvent)
    qrcode = models.CharField(max_length=10, default=0)
    user_type = models.ManyToManyField(UserType, related_name="type_of_user")

    def __str__(self):
        return self.user.first_name

    def get_user(self):
        return self.user.first_name

    def get_organised_event(self):
        return self.organised_event.event.name

    def get_qrcode(self):
        return self.qrcode

    def get_user_type(self):
        types = self.user_type.all()
        type = []
        for t in types:
            type.append(t.name)

        return type
