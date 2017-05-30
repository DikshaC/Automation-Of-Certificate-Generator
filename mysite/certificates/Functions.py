from datetime import datetime

from .models import *
from django.contrib.auth.models import User
from django.db import models


def a():
    print("hi")
    b = input()

    def __str__(self):
        return "hi"


def add_user():
    username = input("Username:")
    password = input("Password:")
    first_name = input("First name:")
    last_name = input("Last name:")
    email = input("Email:")
    type = input("User type:")
    DOB = input("DOB:")
    college = input("college (if any):")

    user1 = User(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
    user1.save()
    profile = Profile(user=user1, DOB=DOB, college=college)
    type_user = UserType.objects.get(name=type)
    type_user.save()
    type_user.user.add(user1)
    profile.save()
    type_user.save()


def add_certificate():
    template = input("Template name:")
    logo = input("logo:")

    certificate = Certificate(template=template, logo=logo)
    certificate.save()


def add_event():
    name = input("name of event:")
    certificate = input("Certificate:")
    c=Certificate.objects.get(template=certificate)
    event = Event(name=name,certificate=c)
    event.save()


def add_organised_event():
    event = input("Event:")
    e = Event.objects.get(name=event)
    start_date = input("start date:")
    end_date = input("end date:")

    num_days = input("Num days:")

    e = OrganisedEvent(event=e, start_date=start_date, end_date=end_date, num_of_days=num_days)
    e.save()


def add_user_certificate_info():
    user1 = input("Enter user:")
    us = User.objects.get(first_name=user1)
    days_attended = input("Enter days attended:")
    qr_code = input("Enter QR_Code:")
    event1 = input("Enter Organise_Event:")
    e = Event.objects.get(name=event1)
    oe = OrganisedEvent.objects.get(event=e)
    u = UserCertificateInfo(user=us, organise_event=oe, qrcode=qr_code, days_attended=days_attended)
    u.save()


def find_user():
    u1 = []
    event2 = input("Enter Organise_Event:")
    e1 = Event.objects.get(name=event2)
    oe1 = OrganisedEvent.objects.get(event=e1)
    u1 = UserCertificateInfo.objects.filter(organise_event=oe1)
    for username in u1:
        print(username.user.first_name)

