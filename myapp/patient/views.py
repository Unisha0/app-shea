from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from hospital.models import Ambulance, Hospital
from .models import Patient, Advertisement, PatientHistory
from .forms import PatientSignupForm, PatientLoginForm
from .serializers import AmbulanceSerializer  # Import the serializer
from django.http import JsonResponse
from math import radians, cos, sin, sqrt, atan2
import heapq

# Signup view for patients
def signup(request):
    if request.method == 'POST':
        form = PatientSignupForm(request.POST)
        if form.is_valid():
            # Get latitude and longitude from POST data (hidden fields)
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')

            # Save patient data without latitude and longitude from the form
            patient = form.save(commit=False)
            patient.password = make_password(form.cleaned_data['password'])
            
            # Assign latitude and longitude from hidden fields
            if latitude:
                patient.latitude = latitude
            if longitude:
                patient.longitude = longitude
                
            patient.save()

            return redirect('patient_login')
    else:
        form = PatientSignupForm()

    return render(request, 'patient/signup.html', {'form': form})

# Login view for patients
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

# Dashboard view
def dashboard(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient_login')
    patient = Patient.objects.get(id=patient_id)
    ads = Advertisement.objects.all()
    return render(request, 'patient/dashboard.html', {'patient': patient, 'ads': ads})

# View for hospital list
def hospital(request):
    hospitals = Hospital.objects.all()
    return render(request, 'patient/hospital.html', {'hospitals': hospitals})

# User account page
def user_account(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient_login')
    patient = Patient.objects.get(id=patient_id)
    return render(request, 'patient/user_account.html', {'patient': patient})

# View for ambulance details
def ambulance(request):
    ambulances = Ambulance.objects.filter(available=True)
    serializer = AmbulanceSerializer(ambulances, many=True)
    return render(request, 'patient/ambulance.html', {'ambulances': serializer.data})

# Help page view
def help_page(request):
    return render(request, 'patient/help_page.html')

# Patient history page
def patient_history(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient_login')
    history = PatientHistory.objects.filter(patient_id=patient_id)
    return render(request, 'patient/patient_history.html', {'history': history})

# Logout view
def logout(request):
    request.session.flush()
    return redirect('patient_login')

# Nearest hospital view
def nearest_hospital(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient_login')

    patient = Patient.objects.get(id=patient_id)

    # Get the nearest hospital and its distance
    nearest_hospital, distance = patient.get_nearest_hospital()

    if nearest_hospital:
        return JsonResponse({
            'nearest_hospital': {
                'name': nearest_hospital.name,
                'address': nearest_hospital.address,
                'latitude': nearest_hospital.latitude,
                'longitude': nearest_hospital.longitude
            },
            'distance': distance
        })
    else:
        return JsonResponse({'error': 'No hospital found or patient location is unavailable'})

# Function for haversine distance calculation
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of Earth in kilometers
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# Function to find nearest hospital using Dijkstra's algorithm (optional)
def dijkstra_shortest_path(start_lat, start_lon):
    hospitals = Hospital.objects.all()
    graph = {}
    for hospital in hospitals:
        graph[hospital.id] = []
        for neighbor in hospitals:
            if hospital != neighbor:
                distance = haversine_distance(hospital.latitude, hospital.longitude, neighbor.latitude, neighbor.longitude)
                graph[hospital.id].append((neighbor.id, distance))

    def dijkstra(start_id):
        distances = {hospital.id: float('inf') for hospital in hospitals}
        previous_nodes = {hospital.id: None for hospital in hospitals}
        distances[start_id] = 0
        queue = [(0, start_id)]

        while queue:
            current_distance, current_id = heapq.heappop(queue)

            if current_distance > distances[current_id]:
                continue

            for neighbor_id, weight in graph[current_id]:
                distance = current_distance + weight
                if distance < distances[neighbor_id]:
                    distances[neighbor_id] = distance
                    previous_nodes[neighbor_id] = current_id
                    heapq.heappush(queue, (distance, neighbor_id))

        return distances, previous_nodes

    start_hospital = Hospital.objects.filter(latitude=start_lat, longitude=start_lon).first()
    if start_hospital:
        distances, previous_nodes = dijkstra(start_hospital.id)
        nearest_hospital_id = min(distances, key=distances.get)
        nearest_hospital = Hospital.objects.get(id=nearest_hospital_id)
        return {
            'nearest_hospital': {
                'name': nearest_hospital.name,
                'address': nearest_hospital.address,
                'latitude': nearest_hospital.latitude,
                'longitude': nearest_hospital.longitude
            },
            'distance': distances[nearest_hospital_id]
        }
    return {'error': 'No hospital found near the given location'}

from django.http import JsonResponse
from .models import Hospital

def get_hospitals(request):
    hospitals = Hospital.objects.all().values('name', 'address', 'latitude', 'longitude')
    return JsonResponse(list(hospitals), safe=False)

