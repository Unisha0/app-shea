from django import forms
from .models import AmbulanceDriver

class AmbulanceDriverSignupForm(forms.ModelForm):
    class Meta:
        model = AmbulanceDriver
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'license_number', 'hospital']

class AmbulanceDriverLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=15, label="Phone Number")
    password = forms.CharField(widget=forms.PasswordInput,  label="Password")
