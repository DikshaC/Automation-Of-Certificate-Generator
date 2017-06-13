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
            user = authenticate(username=form['username'].value(), password=form['password'].value())
            if user is not None:
                return redirect('home/')
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
            return redirect('/')
    else:
        form = UserForm()
        return render(request, "certificates/add_modelform.html", {'form': form})


def edit_user(request):
    return render(request, "certificates/add_modelform.html")


def view_user(request):
    user = User.objects.all()
    context = {"object_list":user}
    return render(request, 'certificates/view_user.html', context)


def add_certificate(request):
    if request.method == "POST":
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            functions.add_certificate(request.FILES['template'], form['title'].value())
            return redirect('/')
    else:
        form = CertificateForm()
        return render(request, "certificates/add_modelform.html", {'form': form})


def edit_certificate(request):
    return render(request, 'certificates/edit_certificate.html')


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
            create_event(form['name'].value(), form['certificate'].value(), form['creator'].value())
            return redirect('/')
    else:
        form = EventForm()
        return render(request, "certificates/add_modelform.html", {'form': form})


def edit_event(request):
    return render(request, "certificates/add_modelform.html")


def view_event(request):
    event=Event.objects.all()
    context = {"object_list": event}
    return render(request, 'certificates/view_event.html', context)


def organise_event(request):
    if request.method == "POST":
        form = OrganisedEventForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            return redirect('/')
    else:
        form = OrganisedEventForm()
        return render(request, "certificates/add_modelform.html", {'form': form})


def edit_organised_event(request):
    return render(request, "certificates/add_modelform.html")


def view_organised_event(request):
    organised_event = OrganisedEvent.objects.all()
    context = {"object_list": organised_event}
    return render(request, 'certificates/view_organised_event.html', context)

