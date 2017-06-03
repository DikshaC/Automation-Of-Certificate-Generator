import csv
import hashlib
import os
import subprocess
import smtplib
from django.core.files import File
from .models import *
from django.contrib.auth.models import User


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
    u = UserCertificateInfo(user=user, organise_event=event, qrcode=qr_code, days_attended=days_attended)
    u.save()
    print(u.user.first_name)
    print(qr_code)


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


def read_csv(name):
    reader = csv.reader(open(name), delimiter=",")
    csv_file = list(reader)[1:]

    for line in csv_file:
        first_name = line[0]
        last_name = line[1]
        username = line[2]
        password = line[3]
        email = line[4]
        type = line[5]
        dob = line[6]
        college = line[7]

        user = User(first_name=first_name, last_name=last_name, username=username, password=password, email=email)
        user.save()

        profile = Profile(user=user, DOB=dob, college=college)
        profile.save()

        type_user = UserType.objects.get(name=type)
        type_user.save()
        type_user.user.add(user)
        type_user.save()

        print(user.first_name)


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
    serial_key = (hashlib.sha1(str(serial_no).encode('utf-8'))).hexdigest()
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


