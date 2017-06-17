import csv
import hashlib
import os
import subprocess
import smtplib
from datetime import datetime
from django.core.mail import EmailMessage
from .models import *
from django.contrib.auth.models import User
import zipfile
from django.conf import settings


def add_user_profile(first_name, last_name, email, dob, college, contact_number):
    """
    Adds a new participant/organiser/etc to the database
    :param first_name: User's first name
    :param last_name:  User's last name
    :param email: The current email-id used for sending certificates
    :param dob: Date Of birth
    :param college: College of the user (If exists)
    :param contact_number: contact mobile number of user

    """
    user = UserProfile(first_name=first_name, last_name=last_name, email=email, dob=dob, college=college,
                       contact_number=contact_number)
    user.save()
    return user


def add_certificate(template, title):
    """
    Adds a new zip folder containing certificate template and it's details.

    :param template: It is the zipped folder to be stored .
    :param title: Title of certificate.
    :return: Returns the certificate object.
    """
    certificate = Certificate(template=template, title=title)
    certificate.save()
    return certificate


def create_event(event, certificate, creator):
    """
    Creates a new event which can be used again for organising an event.

    :param event: The name of the event.
    :param certificate: The certificate class's object.
    :param creator: The user who created this event.
    :return: Return the event object.
    """
    event = Event(name=event, certificate=certificate, creator=creator)
    event.save()
    return event


def organise_event(event, start_date, end_date, organiser, place, participants):
    """
    Adds an event from the event class to be organised.

    :param event: The event class object which is to be organised.
    :param start_date: The starting date of the organised event (Format: Year-month-day, for eg. XXXX-XX-XX )
    :param end_date: The ending date of the organised event (Format: Year-month-day, for eg. XXXX-XX-XX )
    :param organiser: The organiser's name.
    :param place: The place where the event is being organised.
    :param participants: The participating users in the event.
    :return: Returns the object of the organised_event class
    """
    num_days = (end_date-start_date).days
    organised_event = OrganisedEvent(event=event, start_date=start_date, end_date=end_date, num_of_days=num_days,
                                     organiser=organiser, place=place)
    organised_event.save()
    for participant in participants:
        organised_event.participants.add(participant)
        organised_event.save()
    return organised_event


def add_participant(event, participants_email):
    """
    Adds participants/users to the events organised.

    :param event: The organised event name in which participants are to be added
    :param participants_email: The list of participants to be added to an event organised.
    :return: Returns the participants's list which are successfull added to the database
    """
    organised_event = OrganisedEvent.objects.get(event=event)
    for participant_email in participants_email:
        user = UserProfile.objects.get(email=participant_email)
        organised_event.participants.add(user)
        organised_event.save()

    return participants_email


def add_user_certificate_info(user, organised_event, user_type):
    """
    Adds information about the certificate of a user in a particular event

    :param user: User class object.
    :param organised_event: The event object.
    :param user_type: The list of roles played by the user in that event.
    :return:
    """

    user_info = UserCertificateInfo(user=user, organised_event=organised_event)
    user_info.save()
    for types in user_type:
        user_type = UserType.objects.get(name=types)
        user_info.user_type.add(user_type)
        user_info.save()
    return user_info


def zip_to_pdf(certificate):
    """
    to be corrected soon!

    :param certificate:zip file of certificate latex template
    :return:
    """

    file = certificate.template

    path = settings.MEDIA_ROOT
    filename = os.path.basename(file.name)

    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(settings.MEDIA_ROOT)

    folder = filename.split('.')
    folder = folder[0]

    path_folder = path+folder
    file = os.path.join(path_folder, folder+".tex")

    os.chdir(path_folder)

    cmd = ['pdflatex', '-interaction', 'nonstopmode', file]
    proc = subprocess.Popen(cmd)
    proc.communicate()

    file = os.path.join(path_folder,folder+".pdf")
    return file


def read_csv(filename):
    """
    Reads a csv file to add users in the database for a particular event.

    :param filename: The name of the .csv file
            Format (Without spaces in between): first_name,last_name,username,password,email,type,DOB,college
    :return: Returns the first name of the user as a confirmation
    """
    path = settings.MEDIA_ROOT
    file = os.path.join(path, filename)

    file1 = open(file, "r")
    first_line = file1.readline().strip()
    file1.close()

    event = Event.objects.get(name=first_line)
    organised_event = OrganisedEvent.objects.get(event=event)

    reader = csv.reader(open(file), delimiter=";")
    csv_file = list(reader)[1:]

    for line in csv_file:
        email = line[2]
        user_type = line[6].split(',')
        if not UserProfile.objects.filter(email=email):
            first_name = line[0]
            last_name = line[1]
            dob = line[3]
            college = line[4]
            contact_number = line[5]
            add_user_profile(first_name, last_name, email, dob, college, contact_number)

        user = UserProfile.objects.get(email=email)
        add_user_certificate_info(user, organised_event, user_type)


def generate_qrcode(user, organised_event):
    """
    Generates the qrcode for a given user in an organised event
    :param user: The firstname of the user.
    :param organised_event: The name of the organised event.

    """
    user_id = int(user.id)
    hexa1 = hex(user_id).replace('0x', '').zfill(6).upper()
    organised_event_id = int(organised_event.id)
    hexa2 = hex(organised_event_id).replace('0x', '').zfill(6).upper()

    serial_no = '{0}{1}'.format(hexa1, hexa2)
    serial_key = (hashlib.sha256(str(serial_no).encode('utf-8'))).hexdigest()

    uniqueness = False
    num = 5
    qrcode = ""
    while not uniqueness:
        present = UserCertificateInfo.objects.filter(qrcode__startswith=serial_key[0:num])
        if not present:
            qrcode = serial_key[0:num]
            uniqueness = True
        else:
            if present[0].user != user:
                num += 1
            else:  # when a user generates his certificate more than 1 time
                qrcode = serial_key[0:num]
                uniqueness = True

    user_info = UserCertificateInfo.objects.get(user=user, organised_event=organised_event)
    user_info.qrcode = qrcode
    user_info.save()
    return qrcode


def send_email():
    """
    Send email using smtp server and localhost in built in python
    :return: return 1 for success i.e. mail sent.
    """
    email = EmailMessage('Certificate', 'Send Certificate', to=['user@gmail.com'])
    email_obj = email.send()
    return email_obj


def send_certificate(event):
    """
    Sends certificates to the users of a particular event.

    :param event: The name of the event.
    :return: Return the list of user to whom certificate has been sent.
    """
    event = Event.objects.get(name=event)
    organised_event = OrganisedEvent.objects.get(event=event)
    users = organised_event.participants.all()
    for user in users:
        print("Certificate sent to "+user.username)


def check_latex(filename):
    """
    To be completed soon!
    :param filename:
    :return:
    """
    path = settings.MEDIA_ROOT
    latex_file = os.path.join(path, filename)
    os.chdir(path)

    file = open(latex_file, "r")
    content = file.read()
    print(content)
    '''content = content % {'person': 'Diksha'}
    file.close()

    file=open(latex_file,'w')
    file.write(content)
    file.close()
    cmd = ['pdflatex', '-interaction', 'nonstopmode', latex_file]
    proc = subprocess.Popen(cmd)
    proc.communicate()'''
