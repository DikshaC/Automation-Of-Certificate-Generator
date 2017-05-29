from datetime import datetime

from .models import *
from django.contrib.auth.models import User
from django.db import models

def a():
    print("hi")
    b=input()
    def __str__(self):
        return "hi"

def add_user():
    username=input("Username:")
    password=input("Password:")
    first_name = input("First name:")
    last_name = input("Last name:")
    email = input("Email:")
    type = input("User type:")
    DOB = input("DOB:")
    college=input("college (if any):")

    user1 = User(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
    user1.save()
    profile = Profile(user=user1, DOB=DOB, college=college)
    type_user = UserType.objects.get(name=type)
    type_user.save()
    type_user.user.add(user1)
    profile.save()
    type_user.save()


def add_certificate():
    template=input("Template name:")
    logo=input("logo:")

    certificate=Certificate(latex_template=template,logo=logo)
    certificate.save()


def add_event():
    name=input("name of event:")
    certificate=input("Certificate:")
    c=Certificate.objects.get(latex_template=certificate)
    event=Event(name=name,certificate=c)
    event.save()


def add_organised_events():
    event=input("Event:")
    e=Event.objects.get(name=event)
    start_date=input("start date:")
    end_date=input("end date:")


    num_days=input("Num days:")

    e=OrganisedEvent(program=e,start_date=start_date,end_date=end_date,num_of_days=num_days)
    e.save()

    #print(User.objects.all())
    print("Enter users:")
    print("Type 'exit1 to exit'")

    while(input()!="exit1"):
        user=input("Enter user:")
        e.participant.add(user)
        e.save()


