from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from hospital.models import Ambulance, Hospital
from .models import Patient, Advertisement, PatientHistory
from .forms import PatientSignupForm, PatientLoginForm
from .serializers import AmbulanceSerializer  # Import the serializer


def signup(request):
    if request.method == 'POST':
        form = PatientSignupForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.password = make_password(form.cleaned_data['password'])
            patient.save()
            return redirect('patient_login')
    else:
        form = PatientSignupForm()
    return render(request, 'patient/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = PatientLoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            try:
                patient = Patient.objects.get(phone_number=phone_number)
                if check_password(password, patient.password):
                    request.session['patient_id'] = patient.id
                    return redirect('patient_dashboard')
                else:
                    form.add_error(None, 'Invalid credentials')
            except Patient.DoesNotExist:
                form.add_error(None, 'Patient not found')
    else:
        form = PatientLoginForm()
    return render(request, 'patient/login.html', {'form': form})

def dashboard(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient_login')

    patient = Patient.objects.get(id=patient_id)
    ads = Advertisement.objects.all()
    return render(request, 'patient/dashboard.html', {'patient': patient, 'ads': ads})

def hospital(request):
    hospitals = Hospital.objects.all()
    return render(request, 'patient/hospital.html', {'hospitals': hospitals})

def user_account(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient_login')

    patient = Patient.objects.get(id=patient_id)
    return render(request, 'patient/user_account.html', {'patient': patient})

def ambulance(request):
    # Correcting the filter field from 'is_available' to 'available'
    ambulances = Ambulance.objects.filter(available=True)  # Change is_available to available
    
    # Serialize the Ambulance data
    serializer = AmbulanceSerializer(ambulances, many=True)

    # Pass the serialized data to the template
    return render(request, 'patient/ambulance.html', {'ambulances': serializer.data})

def help_page(request):
    return render(request, 'patient/help_page.html')

def patient_history(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient_login')

    history = PatientHistory.objects.filter(patient_id=patient_id)
    return render(request, 'patient/patient_history.html', {'history': history})

def logout(request):
    request.session.flush()
    return redirect('patient_login')

from django.shortcuts import render

def patient_map(request):
    return render(request, "patient/ambulance.html")

