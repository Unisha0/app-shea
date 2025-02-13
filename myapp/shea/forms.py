import re
from django import forms
from .models import AmbulanceDriver
from hospital.models import Hospitaldb
from django.core.exceptions import ValidationError


class AmbulanceDriverSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    hospital = forms.ModelChoiceField(
        queryset=Hospitaldb.objects.all(), 
        empty_label="Select Hospital",
        label="Hospital"
    )

    class Meta:
        model = AmbulanceDriver
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'license_number', 'hospital', 'password']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r'^(97|98)\d{8}$', phone_number):
            raise ValidationError("Phone number must be exactly 10 digits and start with 97 or 98.")
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned_data


class AmbulanceDriverLoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=10,
        label="Phone Number",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        label="Password"
    )

    class AmbulanceDriverLoginForm(forms.Form):
     phone_number = forms.CharField(
        max_length=10,
        label="Phone Number",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        label="Password"
    )