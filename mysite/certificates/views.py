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
            model_instance = form.save(commit=False)
            model_instance.save()
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


def add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            return redirect('/account/home')
    else:
        form = UserForm()
        return render(request, "certificates/add_modelform.html", {'form': form})


def edit_user(request):
    user = User.objects.all()
    context = {"object_list": user}
    return render(request, 'certificates/view_user.html', context)


def view_user(request):
    user = User.objects.all()
    context = {"object_list":user}
    return render(request, 'certificates/view_user.html', context)


def add_certificate(request):
    if request.method == "POST":
        form = CertificateForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            functions.add_certificate(form.cleaned_data['template'], form.cleaned_data['title'])
            return redirect('/account/home')
    else:
        form = CertificateForm()
        return render(request, "certificates/add_modelform.html", {'form': form})


def edit_certificate(request):
    title = request.GET.get('title')
    certificate = Certificate.objects.get(title=title)
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
            model_instance = form.save(commit=False)
            model_instance.save()
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
            functions.organise_event(form.cleaned_data['event'], form.cleaned_data['start_date'], form.cleaned_data['end_date'],
                                     form.cleaned_data['organiser'], form.cleaned_data['place'], form.cleaned_data['participants'])
            return redirect('/account/home')
    else:
        form = OrganisedEventForm()
        return render(request, "certificates/add_modelform.html", {'form': form})


def edit_organised_event(request):
    event = request.GET.get('event')
    organised_event = OrganisedEvent.objects.get(event=Event.objects.get(name=event))
    form = OrganisedEventForm(initial={'event': organised_event.event, 'start_date': organised_event.start_date,
                                       'end_date': organised_event.end_date,
                                       'organiser': organised_event.organiser, 'place': organised_event.place,
                                       'participants': [participant.pk for participant in organised_event.get_participants()]})
    return render(request, 'certificates/add_modelform.html', {'form': form})


def view_organised_event(request):
    organised_event = OrganisedEvent.objects.all()
    context = {"object_list": organised_event}
    return render(request, 'certificates/view_organised_event.html', context)

