from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from . import functions
from django.contrib.auth import authenticate


def home(request):
    return render(request, 'certificates/home.html')


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                return redirect('home/')
            else:
                return render(request, 'certificates/login.html', {'form': form})
        else:
            return render(request, 'certificates/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'certificates/login.html', {'form': form})


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user=User(username=form.cleaned_data['username'],password=form.cleaned_data['password'],email=form.cleaned_data['email'],
                      first_name=form.cleaned_data['first_name'],last_name=form.cleaned_data['last_name'])
            user.save()
            return redirect('/account/home')
    else:
        form = RegistrationForm()
        return render(request, "certificates/register.html", {'form': form})


def add_user_profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            functions.add_user_profile(form.cleaned_data['first_name'],form.cleaned_data['last_name'],form.cleaned_data['email']
                                       ,form.cleaned_data['dob'],form.cleaned_data['college'],form.cleaned_data['contact_number'])
            return redirect('/account/home')
    else:
        form = UserProfileForm()
        return render(request, "certificates/add_modelform.html", {'form': form})


def edit_user_profile(request):
    email = request.GET.get('email')
    user = UserProfile.objects.get(email=email)
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.dob = form.cleaned_data['dob']
            user.college = form.cleaned_data['college']
            user.contact_number = form.cleaned_data['contact_number']
            user.save()
            return redirect('/account/home')
    else:
        form = UserProfileForm(initial={'first_name': user.first_name,'last_name': user.last_name,'email':email, 'dob':user.dob,
                                        'college':user.college,'contact_number':user.contact_number})
        return render(request, 'certificates/add_modelform.html', {'form': form})


def view_user_profile(request):
    user = UserProfile.objects.all()
    context = {"object_list":user}
    return render(request, 'certificates/view_user.html', context)


def add_certificate(request):
    if request.method == "POST":
        form = CertificateForm(request.POST)
        if form.is_valid():
            functions.add_certificate(form.cleaned_data['template'], form.cleaned_data['title'])
            return redirect('/account/home')
    else:
        form = CertificateForm()
        return render(request, "certificates/add_modelform.html", {'form': form})


def edit_certificate(request):
    title = request.GET.get('title')
    certificate = Certificate.objects.get(title=title)
    if request.method == "POST":
        form = CertificateForm(request.POST)
        if form.is_valid():
            certificate.template = form.cleaned_data['template']
            certificate.title = form.cleaned_data['title']
            certificate.save()
            return redirect('/account/home')
    else:
        form = CertificateForm(initial={'title': title,'template': certificate.template})
        return render(request, 'certificates/add_modelform.html', {'form': form})


def view_certificate(request):
    certificate = Certificate.objects.all()
    context = {"object_list": certificate}
    return render(request, 'certificates/view_certificate.html', context)


def add_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            functions.create_event(form.cleaned_data['name'], form.cleaned_data['certificate'], form.cleaned_data['creator'])
            return redirect('/account/home')
        else:
            return render(request, "certificates/add_modelform.html", {'form': form})
    else:
        form = EventForm()
        return render(request, "certificates/add_modelform.html", {'form': form})


def edit_event(request):
    name = request.GET.get('name')
    event = Event.objects.get(name=name)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event.certificate = form.cleaned_data['certificate']
            event.creator = form.cleaned_data['creator']
            event.name = form.cleaned_data['name']
            event.save()
            return redirect('/account/home')
    else:
        form = EventForm(initial={'name': name, 'certificate': event.certificate, 'creator': event.creator})
        return render(request, 'certificates/add_modelform.html', {'form': form})


def view_event(request):
    event=Event.objects.all()
    context = {"object_list": event}
    return render(request, 'certificates/view_event.html', context)


def organise_event(request):
    if request.method == "POST":
        form = OrganisedEventForm(request.POST)
        if form.is_valid():
            functions.organise_event(form.cleaned_data['event'], form.cleaned_data['start_date'],
                                     form.cleaned_data['end_date'],form.cleaned_data['organiser'],
                                     form.cleaned_data['place'], form.cleaned_data['participants'])
            return redirect('/account/home')
    else:
        form = OrganisedEventForm()
        return render(request, "certificates/add_modelform.html", {'form': form})


def edit_organised_event(request):
    event = request.GET.get('event')
    organised_event = OrganisedEvent.objects.get(event=Event.objects.get(name=event))
    if request.method == "POST":
        form = OrganisedEventForm(request.POST)
        if form.is_valid():
            organised_event.event = form.cleaned_data['event']
            organised_event.start_date = form.cleaned_data['start_date']
            organised_event.end_date = form.cleaned_data['end_date']
            organised_event.organiser = form.cleaned_data['organiser']
            organised_event.place = form.cleaned_data['place']
            organised_event.participants = form.cleaned_data['participants']
            organised_event.save()
            return redirect('/account/home')
    else:
        form = OrganisedEventForm(initial={'event': organised_event.event, 'start_date': organised_event.start_date,
                                           'end_date': organised_event.end_date,
                                           'organiser': organised_event.organiser, 'place': organised_event.place,
                                           'participants': [participant.pk for participant in organised_event.get_participants()]})
        return render(request, 'certificates/add_modelform.html', {'form': form})


def view_organised_event(request):
    organised_event = OrganisedEvent.objects.all()
    context = {"object_list": organised_event}
    return render(request, 'certificates/view_organised_event.html', context)

