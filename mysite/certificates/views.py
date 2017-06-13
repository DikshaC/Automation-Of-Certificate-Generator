from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate


def home(request):
    return render(request, 'certificates/home.html')


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            #model_instance = form.save(commit=False)
            #model_instance.save()
            user = authenticate(username=form['username'].value(), password=form['password'].value())
            if user is not None:
                return redirect('home/')
            else:
                return render(request, 'certificates/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'certificates/login.html', {'form': form})


def add_certificate(request):
    if request.method == "POST":
        form = CertificateForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            return redirect('/')
    else:
        form = CertificateForm()
        return render(request, "certificates/my_template.html", {'form': form})


def add_event(request):
    event=Event.objects.all()
    context = {"object_list": event}
    return render(request, 'certificates/event.html', context)