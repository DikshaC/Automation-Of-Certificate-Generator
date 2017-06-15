from django import forms
from material import Layout, Row, Fieldset, Column
from django.forms import ModelForm
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    keep_logged = forms.BooleanField(required=False, label="Keep me logged in")


class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)


    #gender = forms.ChoiceField(choices=((None, ''), ('F', 'Female'), ('M', 'Male'), ('O', 'Other')))
    #receive_news = forms.BooleanField(required=False, label='I want to receive news and special offers')
    #agree_toc = forms.BooleanField(required=True, label='I agree with the Terms and Conditions')

    layout = Layout('username', 'email',
                    Row('password', 'password_confirm'),
                    Fieldset('Personal details',
                             Row('first_name', 'last_name')))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name','last_name', 'dob', 'college', 'email', 'contact_number']


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['template', 'title']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'certificate', 'creator']


class OrganisedEventForm(forms.ModelForm):
    class Meta:
        model = OrganisedEvent
        fields = ['event', 'start_date', 'end_date', 'organiser', 'place', 'participants']


class UserCertificateInfoForm(forms.ModelForm):
        class Meta:
            model = UserCertificateInfo
            fields = ['user', 'organised_event', 'qrcode', 'user_type']