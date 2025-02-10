from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import Hospital, Doctor, DoctorSchedule, Ambulance
from .forms import HospitalSignupForm, HospitalLoginForm, HospitalForm, DoctorForm, DoctorScheduleForm, AmbulanceForm

# Hospital Signup
def hospital_signup(request):
    if request.method == 'POST':
        form = HospitalSignupForm(request.POST)
        if form.is_valid():
            hospital = form.save(commit=False)
            hospital.set_password(form.cleaned_data['password'])
            hospital.save()
            messages.success(request, f"Hospital {hospital.name} registered successfully!")
            return redirect('hospital:login')  # Redirect to login page after successful signup
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
                if hospital.check_password(password):  # Using the check_password method
                    # Save hospital ID and name in session
                    request.session['hospital_id'] = hospital.id
                    request.session['hospital_name'] = hospital.name
                    messages.success(request, f"Welcome to {hospital.name}!")
                    return redirect('hospital:dashboard')  # Redirect to hospital dashboard after successful login
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
        return redirect('hospital:login')  # Redirect to login page if not logged in

    hospital = Hospital.objects.get(id=hospital_id)
    doctors_count = Doctor.objects.filter(hospital=hospital).count()
    ambulances_count = Ambulance.objects.filter(hospital=hospital).count()

    context = {
        'hospital': hospital,
        'doctors_count': doctors_count,
        'ambulances_count': ambulances_count
    }

    return render(request, 'hospital/dashboard.html', context)


# Hospital Logout
def hospital_logout(request):
    logout(request)
    request.session.flush()  # Clear session data after logout
    messages.success(request, "Logged out successfully.")
    return redirect('hospital:login')  # Redirect to login page after logging out

# Manage Hospitals
def manage_hospital(request):
    if not request.session.get('hospital_id'):  # Check if hospital is logged in
        return redirect('hospital:login')  # Redirect to login if not logged in
    hospitals = Hospital.objects.all()
    return render(request, 'hospital/manage_hospital.html', {'hospitals': hospitals})

# Edit Hospital Details
def edit_hospital(request, pk):
    if not request.session.get('hospital_id'):  # Check if hospital is logged in
        return redirect('hospital:login')  # Redirect to login if not logged in

    hospital = get_object_or_404(Hospital, pk=pk)
    if request.method == 'POST':
        form = HospitalForm(request.POST, instance=hospital)
        if form.is_valid():
            form.save()
            messages.success(request, "Hospital details updated successfully!")
            return redirect('hospital:dashboard')  # Redirect to dashboard after update
    else:
        form = HospitalForm(instance=hospital)
    return render(request, 'hospital/edit_hospital.html', {'form': form})

# Manage Doctors
def manage_doctors(request):
    if not request.session.get('hospital_id'):  # Check if hospital is logged in
        return redirect('hospital:login')  # Redirect to login if not logged in

    hospital = Hospital.objects.get(id=request.session['hospital_id'])
    doctors = Doctor.objects.filter(hospital=hospital)
    return render(request, 'hospital/manage_doctors.html', {'doctors': doctors})

# Add or Edit Doctor
def edit_doctor(request, pk=None):
    if not request.session.get('hospital_id'):  # Check if hospital is logged in
        return redirect('hospital:login')  # Redirect to login if not logged in

    if pk:
        doctor = get_object_or_404(Doctor, pk=pk)
    else:
        doctor = None

    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            doctor = form.save(commit=False)
            hospital_id = request.session.get('hospital_id')
            doctor.hospital = Hospital.objects.get(id=hospital_id)
            doctor.save()
            messages.success(request, "Doctor details updated successfully!")
            return redirect('hospital:manage_doctors')  # Redirect after saving doctor details
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'hospital/edit_doctor.html', {'form': form})

# Manage Doctor Schedules
def manage_doctor_schedules(request):
    if not request.session.get('hospital_id'):  # Check if hospital is logged in
        return redirect('hospital:login')  # Redirect to login if not logged in

    hospital = Hospital.objects.get(id=request.session['hospital_id'])
    doctors = Doctor.objects.filter(hospital=hospital)
    return render(request, 'hospital/manage_doctor_schedules.html', {'doctors': doctors})

# Edit Doctor's Schedule
def edit_doctor_schedule(request, doctor_id):
    if not request.session.get('hospital_id'):  # Check if hospital is logged in
        return redirect('hospital:login')  # Redirect to login if not logged in

    doctor = get_object_or_404(Doctor, id=doctor_id)
    if hasattr(doctor, 'schedule'):
        schedule = doctor.schedule
    else:
        schedule = None

    if request.method == 'POST':
        form = DoctorScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.doctor = doctor
            schedule.save()
            messages.success(request, "Doctor's schedule updated successfully!")
            return redirect('hospital:manage_doctor_schedules')  # Redirect after saving schedule
    else:
        form = DoctorScheduleForm(instance=schedule)

    return render(request, 'hospital/edit_doctor_schedule.html', {'form': form, 'doctor': doctor})

# Manage Ambulances
def manage_ambulances(request):
    if not request.session.get('hospital_id'):  # Check if hospital is logged in
        return redirect('hospital:login')  # Redirect to login if not logged in

    hospital = Hospital.objects.get(id=request.session['hospital_id'])
    ambulances = Ambulance.objects.filter(hospital=hospital)
    return render(request, 'hospital/manage_ambulances.html', {'ambulances': ambulances})

# Add or Edit Ambulance
def edit_ambulance(request, pk=None):
    if not request.session.get('hospital_id'):  # Check if hospital is logged in
        return redirect('hospital:login')  # Redirect to login if not logged in

    if pk:
        ambulance = get_object_or_404(Ambulance, pk=pk)
    else:
        ambulance = None

    if request.method == 'POST':
        form = AmbulanceForm(request.POST, instance=ambulance)
        if form.is_valid():
            ambulance = form.save(commit=False)
            hospital_id = request.session.get('hospital_id')
            ambulance.hospital = Hospital.objects.get(id=hospital_id)
            ambulance.save()
            messages.success(request, "Ambulance details updated successfully!")
            return redirect('hospital:manage_ambulances')  # Redirect after saving ambulance details
    else:
        form = AmbulanceForm(instance=ambulance)
    return render(request, 'hospital/edit_ambulance.html', {'form': form})


from django.http import JsonResponse
from hospital.models import Hospitaldb

def hospital_list(request):
    hospitals = Hospitaldb.objects.all().values("name", "speciality", "contact", "address", "latitude", "longitude")
    return JsonResponse(list(hospitals), safe=False)
