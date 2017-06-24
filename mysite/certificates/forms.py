from django import forms
from django.utils.safestring import mark_safe
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label=mark_safe("<strong>User Name</strong>"))
    password = forms.CharField(widget=forms.PasswordInput, label=mark_safe("<strong>Password</strong>"))


class RegistrationForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    username = forms.CharField()
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'dob', 'college', 'email', 'contact_number']


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['template', 'title']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'certificate', 'creator']


class DateInput(forms.DateInput):
    input_type = 'date'


class OrganisedEventForm(forms.ModelForm):
    class Meta:
        model = OrganisedEvent
        fields = ['event', 'start_date', 'end_date', 'organiser', 'place', 'participants']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }


class UserCertificateInfoForm(forms.ModelForm):
    class Meta:
        model = UserCertificateInfo
        fields = ['user', 'organised_event', 'qrcode', 'user_type']


class VerificationForm(forms.Form):
    qrcode = forms.CharField(label=mark_safe("<strong>QR Code</strong>"))


class AddUserForm(forms.Form):
    csvFile=forms.FileField(label=mark_safe("<strong>CSV File</strong>"))
