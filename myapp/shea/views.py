from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import AmbulanceDriverSignupForm, AmbulanceDriverLoginForm
from .models import AmbulanceDriver

# View for ambulance driver signup
def ambulance_driver_signup(request):
    if request.method == 'POST':
        form = AmbulanceDriverSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Signup successful! Please log in.')
            return redirect('ambulance_driver_login')  # Redirect to the login page
    else:
        form = AmbulanceDriverSignupForm()
    return render(request, 'shea/ambulance_driver_signup.html', {'form': form})

# View for ambulance driver login
def ambulance_driver_login(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        
        # Try to authenticate the driver
        try:
            driver = AmbulanceDriver.objects.get(phone_number=phone_number)
            if driver.check_password(password):  # Check password for matching
                login(request, driver)
                return redirect('ambulance_driver_dashboard')  # Redirect to the dashboard
            else:
                messages.error(request, 'Invalid password.')
        except AmbulanceDriver.DoesNotExist:
            messages.error(request, 'Invalid phone number.')

    else:
        form = AmbulanceDriverLoginForm()

    return render(request, 'shea/ambulance_driver_login.html', {'form': form})

# View for ambulance driver logout
def ambulance_driver_logout(request):
    logout(request)
    return redirect('ambulance_driver_login')

# View for ambulance driver dashboard
def ambulance_driver_dashboard(request):
    driver = request.user  # Assuming the driver is logged in and is the user
    # Add any driver-specific data you want to display here, like ambulance assignments, etc.
    return render(request, 'shea/ambulance_driver_dashboard.html', {'driver': driver})

