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
    """
    Adds a new participant/organiser/etc to the database

    :param username: The one to be used for creating the django account
    :param password: Min 8 letter/digits
    :param first_name: User's first name
    :param last_name:  User's last name
    :param email: The current email-id used for sending certificates
    :param user_type: Recognizes the role of the user in the event
    :param dob: Date Of birth
    :param college: College of the user (If exists)

    """
    user = User(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
    user.save()
    profile = Profile(user=user, dob=dob, college=college)
    profile.save()
    type_user = UserType.objects.get(user_type=user_type)
    type_user.save()
    type_user.user.add(user)
    type_user.save()
    return user


def add_certificate(template):
    """
    Adds a new zip folder containing certificate template and it's details.

    :param template: It is the zipped folder to be stored .
    :return: Returns the certificate object.
    """
    certificate = Certificate(template=template)
    certificate.save()
    return certificate


def create_event(name, certificate, creator):
    """
    Creates a new event which can be used again for organising an event.

    :param event: The name of the event.
    :param certificate: The certificate class's object.
    :param creator: The user who created this event.
    :return: Return the event object.
    """
    certificate = Certificate.objects.get(template=certificate)
    user = User.objects.get(username=creator)
    event_obj = Event(event=event, certificate=certificate, creator=user)
    event_obj.save()
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
    start_date1 = datetime.strptime(start_date, "%Y-%m-%d")
    end_date1 = datetime.strptime(end_date, "%Y-%m-%d")
    num_days = (end_date1-start_date1).days
    event = Event.objects.get(event=event)
    user = User.objects.get(username=organiser)
    organised_event = OrganisedEvent(organised_event=event, start_date=start_date, end_date=end_date, num_of_days=num_days, organiser=user, place=place)
    organised_event.save()
    for participant in participants:
        user = User.objects.get(username=participant)
        organised_event.participants.add(user)
        organised_event.save()
    return organised_event


def add_participant(event, participants):
    """
    Adds participants/users to the events organised.

    :param event: The organised event name in which participants are to be added
    :param participants: The list of participants to be added to an event organised.
    :return: Returns the participants's list which are successfull added to the database
    """
    event = Event.objects.get(event=event)
    organised_event = OrganisedEvent.objects.get(organised_event=event)
    for participant in participants:
        user = User.objects.get(username=participant)
        organised_event.participants.add(user)
        organised_event.save()

    return participants


def add_user_certificate_info(user, days_attended, qr_code, organised_event,user_type):
    """
    Adds informations about the certificate of a user in a particular event
    :param user: User class object.
    :param days_attended: Number of days the user attended the event (If exists)
    :param qr_code: The qrcode of the certificate of the user of the event
    :param event: The event object.
    :param user_type: The list of roles played by the user in that event.
    :return:
    """

    user_info = UserCertificateInfo(user=user, organised_event=organised_event, qrcode=qr_code)
    user_info.save()



def zip_to_pdf(filename):
    """
    to be corrected soon!
    :param filename:
    :return:
    """
    path = settings.MEDIA_ROOT
    file = os.path.join(path, filename)

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
    """
    Sends certificates to the users of a particular event.

    :param event: The name of the event.
    :return: Return the list of user to whom certificate has been sent.
    """
    users = []
    event = Event.objects.get(event=event)
    organised_event = OrganisedEvent.objects.get(organised_event=event)
    users = organised_event.participants.all()
    for user in users:
        print("Certificate sent to "+user.username)

    return users

def read_csv(filename):
    """
    Reads a csv file to add users in the database for a particular event.

    :param filename: The name of the .csv file
            Format (Without spaces in between): first_name,last_name,username,password,email,type,DOB,college
    :return: Returns the first name of the user as a confirmation
    """
    path = settings.MEDIA_ROOT
    file = os.path.join(path, filename)

    reader = csv.reader(open(file), delimiter=",")
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

    return first_name


def generate_qrcode(username, organised_event):
    """
    Generates the qrcode for a given user in an organised event

    :param username: The username of the user.
    :param organised_event_name: The name of the organised event.

    """
    user=User.objects.get(username=username)
    user_id = int(user.id)
    hexa1 = hex(user_id).replace('0x', '').zfill(6).upper()

    event=Event.objects.get(event=organised_event)
    organised_event=OrganisedEvent.objects.get(organised_event=event)
    organised_event_id=int(organised_event.id)
    hexa2=hex(organised_event_id).replace('0x','').zfill(6).upper()

    serial_no = '{0}{1}'.format(hexa1,hexa2)
    serial_key = (hashlib.sha256(str(serial_no).encode('utf-8'))).hexdigest()

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
    add_user_certificate_info(user,qrcode,organised_event)


def send_email():
    fromaddr = "abcd@gmail.com"
    toaddr = "abcd@gmail.com"

    msg = "hi! msg "
    #attach = ("csvonDesktp.csv")

    username = "abcd@gmail.com"
    password = "abcd"

    server = smtplib.SMTP('smtp.gmail.com', 587, "abcd@gmail.com")
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddr, msg)
    server.quit()


def check_latex(filename):
    """
    To be completed soon!
    :param filename:
    :return:
    """
    path = settings.MEDIA_ROOT
    latex_file = os.path.join(path, filename)
    os.chdir(path)

    file=open(latex_file,"r")
    content=file.read()
    print(content)
    '''content = content % {'person': 'Diksha'}
    file.close()

    file=open(latex_file,'w')
    file.write(content)
    file.close()


    cmd = ['pdflatex', '-interaction', 'nonstopmode', latex_file]
    proc = subprocess.Popen(cmd)
    proc.communicate()'''
