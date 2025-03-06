import math
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.db.models import Q
from hospital.models import Ambulance, Hospital, Hospitaldb
from .forms import HospitalSignupForm, HospitalLoginForm, HospitalForm, AmbulanceForm
from django.core.mail import send_mail
from patient.models import AmbulanceRequest  # Import from patient app

# Hospital Signup
def hospital_signup(request):
    if request.method == 'POST':
        form = HospitalSignupForm(request.POST)
        if form.is_valid():
            hospital = form.save(commit=False)
            hospital.set_password(form.cleaned_data['password'])
            hospital.save()
            messages.success(request, f"Hospital {hospital.name} registered successfully!")
            return redirect('hospital:login')
    else:
        form = HospitalSignupForm()
    return render(request, 'hospital/signup.html', {'form': form})

# Hospital Login
def hospital_login(request):
    if request.method == 'POST':
        form = HospitalLoginForm(request.POST)
        if form.is_valid():
            pan_number = form.cleaned_data['pan_number']
            password = form.cleaned_data['password']
            try:
                hospital = Hospital.objects.get(pan_number=pan_number)
                if hospital.check_password(password):
                    request.session['hospital_id'] = hospital.id
                    request.session['hospital_name'] = hospital.name
                    messages.success(request, f"Welcome to {hospital.name}!")
                    return redirect('hospital:dashboard')
                else:
                    messages.error(request, "Invalid password.")
            except Hospital.DoesNotExist:
                messages.error(request, "Hospital does not exist.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = HospitalLoginForm()
    return render(request, 'hospital/login.html', {'form': form})

# Hospital Dashboard
def dashboard(request):
    hospital_id = request.session.get('hospital_id')
    if not hospital_id:
        return redirect('hospital:login')

    hospital = Hospital.objects.get(id=hospital_id)
    ambulances_count = Ambulance.objects.filter(hospital=hospital).count()

    context = {
        'hospital': hospital,
        'ambulances_count': ambulances_count
    }

    return render(request, 'hospital/dashboard.html', context)

# Hospital Logout
def hospital_logout(request):
    logout(request)
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect('hospital:login')

# Manage Ambulances
def manage_ambulances(request):
    hospital_id = request.session.get('hospital_id')
    if not hospital_id:
        return redirect('hospital:login')

    hospital = get_object_or_404(Hospital, id=hospital_id)
    ambulances = Ambulance.objects.filter(hospital=hospital)
    return render(request, 'hospital/manage_ambulances.html', {'ambulances': ambulances})

# Notifications Page
def notifications(request):
    if not request.session.get('hospital_id'):
        return redirect('hospital:login')
    return render(request, 'hospital/notifications.html')

# Account Settings Page
def account_settings(request):
    if not request.session.get('hospital_id'):
        return redirect('hospital:login')
    return render(request, 'hospital/account_settings.html')

# Help & Support Page
def help_and_support(request):
    if not request.session.get('hospital_id'):
        return redirect('hospital:login')
    return render(request, 'hospital/help.html')

# Get Hospital List
def hospital_list(request):
    search_term = request.GET.get('search', '').lower()
    patient_lat = float(request.GET.get('lat', 27.7172))
    patient_lon = float(request.GET.get('lon', 85.3240))

    hospitals = Hospitaldb.objects.filter(
        Q(name__icontains=search_term) | Q(speciality__icontains=search_term)
    ).values("id", "name", "speciality", "contact", "address", "latitude", "longitude")

    hospitals = sorted(hospitals, key=lambda hospital: haversine_distance(
        patient_lat, patient_lon, hospital['latitude'], hospital['longitude']
    ))

    return JsonResponse(list(hospitals), safe=False)

# Haversine formula for distance calculation
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    dLat = (lat2 - lat1) * (math.pi / 180)
    dLon = (lon2 - lon1) * (math.pi / 180)
    lat1 = lat1 * (math.pi / 180)
    lat2 = lat2 * (math.pi / 180)

    a = (math.sin(dLat / 2) ** 2) + math.cos(lat1) * math.cos(lat2) * (math.sin(dLon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

# View all pending ambulance requests for a hospital
def view_ambulance_requests(request):
    hospital_id = request.session.get('hospital_id')
    if not hospital_id:
        return redirect('hospital:login')

    hospital = get_object_or_404(Hospital, id=hospital_id)
    requests = AmbulanceRequest.objects.filter(hospital=hospital, status='Pending')

    return render(request, 'hospital/notifications.html', {'requests': requests})

# Accept or reject ambulance request
def respond_to_request(request, request_id, response):
    hospital_id = request.session.get('hospital_id')
    if not hospital_id:
        return redirect('hospital:login')

    ambulance_request = get_object_or_404(AmbulanceRequest, id=request_id)

    # Ensure hospital is authorized to handle the request
    if ambulance_request.hospital.id != hospital_id:
        messages.error(request, "Unauthorized action.")
        return redirect('hospital:notifications')

    if response == 'accept':
        ambulance_request.status = 'Accepted'
        message = "Your ambulance request has been accepted."
    elif response == 'reject':
        ambulance_request.status = 'Rejected'
        message = "Your ambulance request has been rejected."
    else:
        messages.error(request, "Invalid response.")
        return redirect('hospital:notifications')

    ambulance_request.save()

    # Send email notification
    send_mail(
        subject="Ambulance Request Update",
        message=message,
        from_email="no-reply@shea.com",
        recipient_list=[ambulance_request.patient_email],  # Assuming the request has a patient email field
        fail_silently=True
    )

    messages.success(request, f"Request {response}ed successfully.")
    return redirect('hospital:notifications')
    # In views.py

def profile(request):
    hospital_id = request.session.get('hospital_id')
    if not hospital_id:
        return redirect('hospital:login')  # Redirect to login if not logged in

    hospital = get_object_or_404(Hospital, id=hospital_id)

    context = {
        'hospital': hospital
    }

    return render(request, 'hospital/profile.html', context)

