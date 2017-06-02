import os
import subprocess
import smtplib

from django.core.files import File
from django.core.files.storage import FileSystemStorage

from datetime import datetime

from .models import *
from django.contrib.auth.models import User
from django.db import models


def add_user(username, password, first_name, last_name, email, user_type, dob, college):
    user1 = User(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
    user1.save()
    profile = Profile(user=user1, DOB=dob, college=college)
    type_user = UserType.objects.get(name=user_type)
    type_user.save()
    type_user.user.add(user1)
    profile.save()
    type_user.save()
    return user1


def add_certificate(template):
    c = Certificate(template=template)
    c.save()
    return c


def create_event(name, certificate, creator):
    c = Certificate.objects.get(template=certificate)
    e = Event(name=name,certificate=c, creator=creator)
    e.save()
    return e


def organise_event(event, start_date, end_date, num_days, organiser, place, participants):
    e = Event.objects.get(name=event)
    oe = OrganisedEvent(event=e, start_date=start_date, end_date=end_date, num_of_days=num_days, organiser=organiser, place=place)
    oe.save()
    for participant in participants:
        u = User.objects.get(username=participant)
        oe.participants.add(u)
        oe.save()
    return oe


def add_participant(event, participants):
    e = Event.objects.get(name=event)
    oe = OrganisedEvent.objects.get(event=e)
    for participant in participants:
        u = User.objects.get(username=participant)
        oe.participants.add(u)
        oe.save()


def add_user_certificate_info(user, days_attended, qr_code, event):
    us = User.objects.get(first_name=user)
    e = Event.objects.get(name=event)
    oe = OrganisedEvent.objects.get(event=e)
    u = UserCertificateInfo(user=us, organise_event=oe, qrcode=qr_code, days_attended=days_attended)
    u.save()
    return u


def template_to_pdf():
    path = "C:/Users/aditi/PycharmProjects/new_djangoTest/mysite/certificates"
    file = os.path.join(path,"exam.tex")
    tex_file = open(file,"r")

    #pdf, info = texcaller.convert(latex, 'LaTeX', 'PDF', 5)

    cmd = ['pdflatex', '-interaction', 'nonstopmode',file]
    proc = subprocess.Popen(cmd)
    proc.communicate()

    u = Certificate(logo="abc")
    path = "C:/Users/aditi/PycharmProjects/new_djangoTest/mysite/media/aditi"
    file = os.path.join(path,"exam.pdf")
    file1 = File(open(file,"r"))
    u.template = file1
    u.save()


def send_certificate(event):
    users = []
    e = Event.objects.get(name=event)
    oe = OrganisedEvent.objects.get(event=e)
    users = oe.participants.all()
    for user in users:
        print("Certificate sent to "+user.username)


def send_email():
    fromaddr = "soniaditi1397@gmail.com"
    toaddr = "soniaditi1397@gmail.com"

    msg = "hi! msg "
    #attach = ("csvonDesktp.csv")

    username = "soniaditi1397@gmail.com"
    password = "abcd"

    server = smtplib.SMTP('smtp.gmail.com',587,"soniaditi1397@gmail.com")
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddr, msg)
    server.quit()