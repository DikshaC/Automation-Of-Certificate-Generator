import csv
import hashlib
import os
import subprocess
import smtplib

from datetime import datetime

from .models import *
from django.contrib.auth.models import User
import zipfile
from django.conf import settings


def add_user(username, password, first_name, last_name, email, user_type, dob, college):
    user = User(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
    user.save()
    profile = Profile(user=user, DOB=dob, college=college)
    type_user = UserType.objects.get(name=user_type)
    type_user.save()
    type_user.user.add(user)
    profile.save()
    type_user.save()
    return user


def add_certificate(template):
    certificate = Certificate(template=template)
    certificate.save()
    return certificate


def create_event(name, certificate, creator):
    certificate = Certificate.objects.get(template=certificate)
    user = User.objects.get(username=creator)
    event = Event(name=name, certificate=certificate, creator=user)
    event.save()
    return event


def organise_event(event, start_date, end_date, organiser, place, participants):
    start_date1 = datetime.strptime(start_date,"%Y-%m-%d")
    end_date1 = datetime.strptime(end_date, "%Y-%m-%d")
    num_days = (end_date1-start_date1).days
    event = Event.objects.get(name=event)
    user = User.objects.get(username=organiser)
    organised_event = OrganisedEvent(event=event, start_date=start_date, end_date=end_date, num_of_days=num_days, organiser=user, place=place)
    organised_event.save()
    for participant in participants:
        user = User.objects.get(username=participant)
        organised_event.participants.add(user)
        organised_event.save()
    return organised_event


def add_participant(event, participants):
    event = Event.objects.get(name=event)
    organised_event = OrganisedEvent.objects.get(event=event)
    for participant in participants:
        u = User.objects.get(username=participant)
        organised_event.participants.add(u)
        organised_event.save()


def add_user_certificate_info(user, days_attended, qr_code, event):
    user_info = UserCertificateInfo(user=user, organise_event=event, qrcode=qr_code, days_attended=days_attended)
    user_info.save()
    print(user_info.user.first_name)
    print(qr_code)


def zip_to_pdf(filename):
    path = settings.MEDIA_ROOT
    file = os.path.join(path,filename)

    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(settings.MEDIA_ROOT)

    folder = filename.split('.')
    folder = folder[0]

    path_folder = path+folder
    file = os.path.join(path_folder,folder+".tex")

    os.chdir(path_folder)

    cmd = ['pdflatex', '-interaction', 'nonstopmode', file]
    proc = subprocess.Popen(cmd)
    proc.communicate()

    file = os.path.join(path_folder,folder+".pdf")

    certificate = Certificate(title="abc")
    certificate.template = file
    certificate.save()


def send_certificate(event):
    users = []
    event = Event.objects.get(name=event)
    organised_event = OrganisedEvent.objects.get(event=event)
    users = organised_event.participants.all()
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


def read_csv(name):
    reader = csv.reader(open(name), delimiter=",")
    csv_file = list(reader)[1:]

    for line in csv_file:
        first_name = line[0]
        last_name = line[1]
        username = line[2]
        password = line[3]
        email = line[4]
        user_type = line[5]
        dob = line[6]
        college = line[7]
        add_user(username, password, first_name, last_name, email, user_type, dob, college)


def generate_qrcode(username,organised_event_name):
    user=User.objects.get(username=username)
    user_id = int(user.id)
    hexa1 = hex(user_id).replace('0x', '').zfill(6).upper()
    print(hexa1)

    event=Event.objects.get(name=organised_event_name)
    organised_event=OrganisedEvent.objects.get(event=event)
    organised_event_id=int(organised_event.id)
    hexa2=hex(organised_event_id).replace('0x','').zfill(6).upper()
    print(hexa2)

    serial_no = '{0}{1}'.format(hexa1,hexa2)
    serial_key = (hashlib.sha256(str(serial_no).encode('utf-8'))).hexdigest()
    print(serial_key)

    uniqueness = False
    num = 5
    while not uniqueness:
        present = UserCertificateInfo.objects.filter(qrcode__startswith=serial_key[0:num])
        if not present:
            qrcode = serial_key[0:num]
            uniqueness = True
        else:
            if present[0].user!=user:
                num += 1
            else:  # when a user generates his certificate more than 1 time
                qrcode = serial_key[0:num]
                uniqueness=True
    add_user_certificate_info(user,2,qrcode,organised_event)


def check_latex(filename):
    path = settings.MEDIA_ROOT
    file = os.path.join(path, filename)
    os.chdir(path)

    file=open(file,"w")
    content=file.read()

    cmd = ['pdflatex', '-interaction', 'nonstopmode', file]
    proc = subprocess.Popen(cmd)
    proc.communicate()
