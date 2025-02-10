from django import forms
from .models import Patient, UserAccountSettings

class PatientSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = Patient
        fields = ['name', 'email', 'phone_number', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class PatientLoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=10,
        label="Phone Number",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        label="Password"
    )


class PatientUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, label="Profile Picture")
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = Patient
        fields = ['name', 'email', 'phone_number', 'profile_picture']


class UserAccountSettingsForm(forms.ModelForm):
    notifications_enabled = forms.BooleanField(
        required=False,
        label="Enable Notifications",
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = UserAccountSettings
        fields = ['notifications_enabled']
