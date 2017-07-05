from __future__ import unicode_literals
import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from mysite import settings
from .forms import *
from .models import *
from . import functions
from django.contrib.auth import authenticate, logout, login as LOGIN, update_session_auth_hash


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'certificates/index.html')
    else:
        return redirect('/account/home')


@login_required(login_url='/account')
def home(request):
    if request.user.is_authenticated():
        return render(request, 'certificates/home.html')
    else:
        return redirect('/account')


def login(request):
    if not request.user.is_authenticated():
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(request, username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'])
                if user is not None:
                    LOGIN(request, user)
                    return redirect('/account/home')
                else:
                    return render(request, 'certificates/login.html', {'form': form})
            else:
                return render(request, 'certificates/login.html', {'form': form})
        else:
            form = LoginForm()
            return render(request, 'certificates/login.html', {'form': form})
    else:
        return redirect('/account/home')


def logout_user(request):
    logout(request)
    return redirect('/account')


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User(username=form.cleaned_data['username'], password=form.cleaned_data['password'],
                        email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            user.save()
            return redirect('/account/home')
        else:
            form = RegistrationForm()
            return render(request, "certificates/register.html", {'form': form})
    else:
        form = RegistrationForm()
        return render(request, "certificates/register.html", {'form': form})


def profile(request):
    user = request.user
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, 'Your proflie was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Choose another username or email!')
            return redirect('profile')

    else:
        form = UserForm(initial={'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
                                 'username': user.username})
        return render(request, 'certificates/my_profile.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Password not updated! try again')
            form = PasswordChangeForm(request.user)
            return render(request, 'certificates/add_modelform.html', {'form': form})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'certificates/add_modelform.html', {'form': form})


def add_user_profile(request):
    if request.method == "POST":
        form = AddUserForm(request.POST, request.FILES)
        if form.is_valid():
            csv = request.FILES['csvFile']
            path = default_storage.save('abc.csv', ContentFile(csv.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            error_message = functions.read_csv(tmp_file)
            if error_message == "list_index_error":
                messages.error(request, "Please check the format of csv file and try again!")

            else:
                messages.success(request, 'User added successfully! Add next')
                form = AddUserForm()
            return render(request, "certificates/add_user.html", {'form': form})
        else:
            messages.error(request, 'User not added, try again!')
            return render(request, "certificates/add_user.html", {'form': form})
    else:
        form = AddUserForm()
        return render(request, "certificates/add_user.html", {'form': form})


def edit_user_profile(request):
    email = request.GET.get('email')
    user = UserProfile.objects.get(email=email)

    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.dob = form.cleaned_data['dob']
            user.college = form.cleaned_data['college']
            user.contact_number = form.cleaned_data['contact_number']
            user.save()
            messages.success(request, 'User information updated successfully !')
            return redirect('view_user_profile')
        else:
            messages.error(request, 'Participant information not updated! check fields again!')
            form = UserProfileForm(initial={'first_name': user.first_name, 'last_name': user.last_name, 'email': email,
                                            'dob': user.dob, 'college': user.college,
                                            'contact_number': user.contact_number})
            return render(request, 'certificates/edit_delete_modelform.html', {'form': form})

    else:
        form = UserProfileForm(initial={'first_name': user.first_name, 'last_name': user.last_name, 'email': email,
                                        'dob': user.dob, 'college': user.college,
                                        'contact_number': user.contact_number})
        context = {'user': user, 'form': form, 'type': "user_profile"}
        return render(request, 'certificates/edit_delete_modelform.html', context)


def view_user_profile(request):
    user = UserProfile.objects.all()
    context = {"object_list": user}
    return render(request, 'certificates/view_user.html', context)


def delete_user_profile(request):
    email = request.GET.get('email')
    UserProfile.objects.get(email=email).delete()
    messages.success(request, 'User deleted successfully!')
    return redirect('view_user_profile')


def add_certificate(request):
    if request.method == "POST":
        form = CertificateForm(request.POST, request.FILES)
        file = request.FILES['template']
        if form.is_valid():
            functions.add_certificate(file, form.cleaned_data['title'])
            messages.success(request, 'Certificate ' + form.cleaned_data['title'] + ' added successfully! Add next')
            form = CertificateForm()
            return render(request, "certificates/add_certificate.html", {'form': form})
        else:
            messages.error(request, "Certificate not added!")
            return render(request, "certificates/add_certificate.html", {'form': form})
    else:
        form = CertificateForm()
        return render(request, "certificates/add_certificate.html", {'form': form})


def edit_certificate(request):
    title = request.GET.get('title')
    certificate = Certificate.objects.get(title=title)
    if request.method == "POST":
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            certificate.template = request.FILES['template']
            certificate.title = form.cleaned_data['title']
            certificate.save()
            messages.success(request, 'Certificate updated successfully !')
            return redirect('view_certificate')
        else:
            messages.error(request, 'certificate not updated! try again')
            form = CertificateForm(initial={'title': title, 'template': certificate.template})
            return render(request, 'certificates/edit_delete_modelform.html', {'form': form})

    else:
        form = CertificateForm(initial={'title': title, 'template': certificate.template})
        context = {'certificate': certificate, 'form': form, 'type': "certificate"}
        return render(request, 'certificates/edit_delete_modelform.html', context)


def view_certificate(request):
    certificate = Certificate.objects.all()
    context = {"object_list": certificate}
    return render(request, 'certificates/view_certificate.html', context)


def delete_certificate(request):
    title = request.GET.get('title')
    Certificate.objects.get(title=title).delete()
    messages.success(request, 'Certificate deleted successfully!')
    return redirect('view_certificate')


def send_certificate(request):
    organised_event = OrganisedEvent.objects.all()
    context = {"object_list": organised_event}
    return render(request, 'certificates/send_certificate.html', context)


def send_email(request):
    pk = request.GET.get('oe_pk')
    organised_event = OrganisedEvent.objects.get(pk=pk)
    certificate = organised_event.event.certificate

    if request.GET.get('type') == "All":
        participants = organised_event.get_participants()

    else:
        participant_id = request.GET.get("participant_pk")
        participants = UserProfile.objects.filter(pk=participant_id)

    try:
        functions.send_email(participants, certificate, organised_event)
    except:
        participants = organised_event.get_participants()
        context = {"participants": participants, "organised_event": organised_event}
        user_info_list = []
        for participant in participants:
            user_info = UserCertificateInfo.objects.get(user=participant, organised_event=organised_event)
            user_info_list.append(user_info.email_sent_status)

        context["list1"] = zip(participants, user_info_list)
        messages.success(request, "Mail Sent Successfully!")
        return render(request, 'certificates/show_participant.html', context)

    participants = organised_event.get_participants()
    context = {"participants": participants,"organised_event":organised_event}
    user_info_list = []
    for participant in participants:
        user_info = UserCertificateInfo.objects.get(user=participant, organised_event=organised_event)
        user_info_list.append(user_info.email_sent_status)

    context["list1"] = zip(participants, user_info_list)
    return render(request, 'certificates/show_participant.html', context)


def show_participant(request):
    pk = request.GET.get('oe_pk')
    organised_event = OrganisedEvent.objects.get(pk=pk)
    participants = organised_event.get_participants()
    context = {"participants": participants, "organised_event": organised_event}
    user_info_list = []
    for participant in participants:
        user_info = UserCertificateInfo.objects.get(user=participant,organised_event=organised_event)
        user_info_list.append(user_info.email_sent_status)
    context["list1"] = zip(participants, user_info_list)
    return render(request, 'certificates/show_participant.html', context)


def add_event(request):
    creator = request.user
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            functions.create_event(form.cleaned_data['name'], form.cleaned_data['certificate'],
                                   creator)
            messages.success(request, 'Event '+form.cleaned_data['name']+' added successfully! Add next')
            form = EventForm()
            return render(request, "certificates/add_event.html", {'form': form})
        else:
            messages.error(request, "event not added! try again")
            return render(request, "certificates/add_event.html", {'form': form})
    else:
        form = EventForm()
        return render(request, "certificates/add_event.html", {'form': form})


def edit_event(request):
    name = request.GET.get('name')
    event = Event.objects.get(name=name)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event.certificate = form.cleaned_data['certificate']
            event.name = form.cleaned_data['name']
            event.save()
            messages.success(request, 'Event updated successfully !')
            return redirect('view_event')
        else:
            messages.error(request, 'Event not updated! try again')
            form = EventForm(initial={'name': name, 'certificate': event.certificate})
            return render(request, 'certificates/edit_delete_modelform.html', {'form': form})
    else:
        form = EventForm(initial={'name': name, 'certificate': event.certificate})
        context = {'event': event, 'form': form, 'type': "event"}
        return render(request, 'certificates/edit_delete_modelform.html', context)


def view_event(request):
    #user = request.user
    #event=Event.objects.filter(creator=user)
    event = Event.objects.all()
    context = {"object_list": event}
    return render(request, 'certificates/view_event.html', context)


def delete_event(request):
    name = request.GET.get('name')
    Event.objects.get(name=name).delete()
    messages.success(request, 'Event deleted successfully!')
    return redirect('view_event')


def organise_event(request):
    if request.method == "POST":
        form = OrganisedEventForm(request.POST)
        if form.is_valid():
            functions.organise_event(form.cleaned_data['event'], form.cleaned_data['start_date'],
                                     form.cleaned_data['end_date'], form.cleaned_data['organiser'],
                                     form.cleaned_data['place'], form.cleaned_data['participants'])
            messages.success(request, 'Organised Event added successfully! Add next')
            form = OrganisedEventForm()
            return render(request, "certificates/add_organised_event.html", {'form': form})
        else:
            messages.error(request, "Organised Event not added! try again")
            return render(request, "certificates/add_organised_event.html", {'form': form})
    else:
        form = OrganisedEventForm()
        return render(request, "certificates/add_organised_event.html", {'form': form})


def edit_organised_event(request):
    pk = request.GET.get('oe_pk')
    organised_event = OrganisedEvent.objects.get(pk=pk)
    if request.method == "POST":
        form = OrganisedEventForm(request.POST)
        if form.is_valid():
            organised_event.event = form.cleaned_data['event']
            organised_event.start_date = form.cleaned_data['start_date']
            organised_event.end_date = form.cleaned_data['end_date']
            organised_event.organiser = form.cleaned_data['organiser']
            organised_event.place = form.cleaned_data['place']
            organised_event.participants = form.cleaned_data['participants']
            organised_event.num_of_days = (organised_event.end_date-organised_event.start_date).days
            organised_event.save()
            messages.success(request, 'Organised Event updated successfully !')
            return redirect('view_organised_event')
        else:
            messages.error(request, "Organised Event not updated! try again")
            form = OrganisedEventForm(initial={'event': organised_event.event, 'start_date': organised_event.start_date,
                                               'end_date': organised_event.end_date,
                                               'organiser': organised_event.organiser, 'place': organised_event.place,
                                               'participants':
                                                   [participant.pk for participant in
                                                    organised_event.get_participants()]})
            return render(request, 'certificates/edit_delete_modelform.html', {'form': form})
    else:
        form = OrganisedEventForm(initial={'event': organised_event.event, 'start_date': organised_event.start_date,
                                           'end_date': organised_event.end_date,
                                           'organiser': organised_event.organiser, 'place': organised_event.place,
                                           'participants':
                                               [participant.pk for participant in organised_event.get_participants()]})
        context = {'organised_event': organised_event, 'form': form, 'type': "organised_event"}
        return render(request, 'certificates/edit_delete_modelform.html', context)


def view_organised_event(request):
    '''user = request.user
    events = Event.objects.filter(creator=user)
    organised_event = []
    for event in list():
        organised_events = OrganisedEvent.objects.filter(event=event)
        for organisedEvent in organised_events:
            organised_event.append(organisedEvent)'''
    organised_event = OrganisedEvent.objects.all()

    context = {"object_list": organised_event}
    return render(request, 'certificates/view_organised_event.html', context)


def delete_organised_event(request):
    pk = request.GET.get('oe_pk')
    OrganisedEvent.objects.get(pk=pk).delete()
    messages.success(request, 'Organised Event deleted successfully!')
    return redirect('view_organised_event')


def verify(request):
    if request.method == "POST":
        form = VerificationForm(request.POST)
        if form.is_valid():
            qrcode = form.cleaned_data['qrcode']
            user_info = UserCertificateInfo.objects.get(qrcode=qrcode)
            user = user_info.user
            context = {'user': user, 'organised_event': user_info.organised_event}
            return render(request, 'certificates/verify_user.html', context)
        else:
            return render(request, "certificates/verify.html", {'form': form})
    else:
        form = VerificationForm()
        return render(request, "certificates/verify.html", {'form': form})


def preview(request):
    title = request.GET.get('title')
    certificate = Certificate.objects.get(title=title)

    filename, path_folder = functions.unzip_folder(certificate)
    pdf_filename = functions.preview_certificate(filename, path_folder)

    path_file = os.path.join(path_folder, pdf_filename)
    with open(path_file, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = pdf_filename
        test_name = pdf_filename.split('.')[0]
        functions.clean_certificate_files(test_name, path_folder)
        return response
