import csv
import hashlib
import os
import subprocess
from django.core.mail import EmailMessage
from string import Template
from django.http import HttpResponse
from .models import *
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
    :return: Returns the event object.
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


def add_participant(organised_event_pk, participants_email):
    """
    Adds participants/users to the events organised.
    :param organised_event_pk: Organised event'd id
    :param participants_email: The list of participants to be added to an event organised.
    :return: Returns the participants's list which are successfully added to the database
    """
    organised_event = OrganisedEvent.objects.get(pk=organised_event_pk)
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
    :return: Returns the UserCertificateInfo object
    """

    user_info = UserCertificateInfo(user=user, organised_event=organised_event)
    user_info.save()
    for types in user_type:
        user_type = UserType.objects.get(name=types)
        user_info.user_type.add(user_type)
        user_info.save()
    return user_info


#TODO: add organised event primary key things here
def read_csv(file):
    """
    Reads a csv file to add users in the database for a particular event.
    Also deletes the .csv file from database.

    :param file: The name of the .csv file
            Format (Without spaces in between):
            First line: The name of the organised event without inverted commas
            Second line (onwards):
            first_name,last_name,username,password,email,user_type(s)[separated by ',' if more than 1 type ],DOB,college
    :return: Returns nothing
    """
    path = settings.MEDIA_ROOT
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
        organised_event.participants.add(user)
        add_user_certificate_info(user, organised_event, user_type)

    filename = os.path.basename(file)
    os.chdir(path)
    os.remove('abc.csv')


def generate_qrcode(user, organised_event):
    """
    Generates the qrcode for a given user in an organised event
    :param user: The first name of the user.
    :param organised_event: The name of the organised event.

    :return: Returns the qrcode of the user
    """

    user_info = UserCertificateInfo.objects.get(user=user, organised_event=organised_event)
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
            if user_info not in present:
                num += 1
            else:  # when a user generates his certificate more than 1 time
                qrcode = user_info.qrcode
                uniqueness = True

    link_qrcode = 'www.fossee.in/account/verify/'+qrcode
    #user_info = UserCertificateInfo.objects.get(user=user, organised_event=organised_event)
    #user_info.qrcode = qrcode
    #user_info.save()
    return link_qrcode,qrcode


def unzip_folder(certificate):
    """
    Unzips the zipped folder containing latex file and related stuffs.
    :param certificate: The certificate object whose template (zipped file) has to be unzipped.
    :return: Returns filename and the path of the file
    """

    file = certificate.template

    path = settings.MEDIA_ROOT
    filename = os.path.basename(file.name)

    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(settings.MEDIA_ROOT)

    folder = filename.split('.')
    folder = folder[0]

    path_folder = path+folder
    filename=folder+".tex"
    return filename, path_folder


def send_email(participants, certificate, organised_event):
    """
    Sends email to the participants of a particular organised event.

    :param participants: List of participants to whom certificate will be sent
    :param certificate: The certificate object whose template has to be used to send certificates
    :param organised_event: The organised event object whose certificate has to be sent.
    :return: None
    """
    latex_file, path_folder = unzip_folder(certificate)
    status = []
    for participant in participants:
        participant = participant
        create_certificate(latex_file, participant, path_folder, organised_event)
        email = EmailMessage('Certificate', 'Send Certificate', to=[participant.email])
        email_obj = email.send()
        if email_obj:
            status.append(1)
        else:
            status.append(0)
        clean_certificate_files(participant.first_name, path_folder)
    return status

def create_certificate(latex_template, participant, path_folder, organised_event):
    """
    Creates the certificate from latex template and returns the name of the certificate.

    :param latex_template:The latex file (.tex) which has to converted to pdf
    :param participant: The participant (UserProfile object) whose certificate has to be created
    :param path_folder: The path of the folder containing latex file (.tex)
    :param organised_event: The organised event object whose certificate has to be created for the participant

    :return: Returns the name of the pdf file : Default: (Name of the participant).pdf
    """


    link_qrcode, qrcode = generate_qrcode(participant,organised_event)
    user_info = UserCertificateInfo.objects.get(user=participant,organised_event=organised_event)
    user_info.qrcode=qrcode
    user_info.save()

    latex_file = os.path.join(path_folder, latex_template)
    file = open(latex_file, "r")
    content = Template(file.read())
    print(file)
    file.close()

    content_tex = content.safe_substitute(name=participant.first_name+" "+participant.last_name,
                                          event_name=organised_event.event.name, qrcode=qrcode,
                                          link_qrcode=link_qrcode,
                                          start_date=organised_event.start_date,
                                          end_date=organised_event.end_date,num_days=organised_event.num_of_days,
                                          user_type=user_info.user_type)

    user_latex_file = os.path.join(path_folder, participant.first_name + '.tex')
    user_file = open(user_latex_file, 'w+')
    user_file.write(content_tex)
    user_file.close()

    os.chdir(path_folder)
    cmd = ['pdflatex', '-shell-escape', user_latex_file]
    proc = subprocess.Popen(cmd)
    proc.communicate()
    return participant.first_name + '.pdf'


def clean_certificate_files(first_name, path):
    """
    Clears the unwanted files after pdf is generated from latex.
    :param first_name:The name of the participant (as all the files are created with participant's name)
    :param path: The path of the folder where pdf has created(or tex file is stored)
    :return: Returns none
    """
    os.chdir(path)
    #os.remove(first_name + '.pdf')
    os.remove(first_name + '-pics.pdf')
    os.remove(first_name + '.aux')
    os.remove(first_name + '.log')
    os.remove(first_name + '.tex')


def preview_certificate(latex_template, path_folder, event):
    latex_file = os.path.join(path_folder, latex_template)
    file = open(latex_file, "r")
    content = Template(file.read())
    print(file)
    file.close()

    content_tex = content.safe_substitute(name="testFirstName"+" "+"testLastName",
                                          qrcode="testQrcode0123", link_qrcode="www.fossee.in/testPreview",
                                          start_date="2017-03-30",
                                          end_date="2017-03-31", num_days=1,
                                          user_type="testParticipant")

    user_latex_file = os.path.join(path_folder, "testFirstName" + '.tex')
    user_file = open(user_latex_file, 'w+')
    user_file.write(content_tex)
    user_file.close()

    os.chdir(path_folder)
    cmd = ['pdflatex' ,'-shell-escape', user_latex_file]
    proc = subprocess.Popen(cmd)
    proc.communicate()
    return "testFirstName.pdf"
