from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AmbulanceDriverSignupForm, AmbulanceDriverLoginForm
from .models import AmbulanceDriver

# 🚑 SIGNUP VIEW 🚑
def ambulance_driver_signup(request):
    if request.method == "POST":
        form = AmbulanceDriverSignupForm(request.POST)
        if form.is_valid():
            driver = form.save(commit=False)  # Don't save yet
            driver.set_password(form.cleaned_data["password"])  # Hash password
            driver.save()  # Now save
            messages.success(request, "Signup successful! You can now log in.")
            return redirect("shea:ambulance_driver_login")  # Redirect using namespace
        else:
            messages.error(request, "Error in form submission. Please check your details.")
    else:
        form = AmbulanceDriverSignupForm()
    
    return render(request, "shea/ambulance_driver_signup.html", {"form": form})

# 🚑 LOGIN VIEW 🚑
def ambulance_driver_login(request):
    if request.session.get("driver_id"):  # Prevent logged-in users from seeing login page
        return redirect("shea:ambulance_driver_dashboard")

    if request.method == "POST":
        form = AmbulanceDriverLoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get("phone_number")
            password = form.cleaned_data.get("password")

            try:
                driver = AmbulanceDriver.objects.get(phone_number=phone_number)
                if driver.check_password(password):  # Check hashed password
                    request.session["driver_id"] = driver.id  # Store in session
                    messages.success(request, "Login successful!")
                    return redirect("shea:ambulance_driver_dashboard")  # Redirect using namespace
                else:
                    messages.error(request, "Incorrect password!")
            except AmbulanceDriver.DoesNotExist:
                messages.error(request, "Invalid phone number or password!")
        else:
            messages.error(request, "Please check the form for errors.")
    
    else:
        form = AmbulanceDriverLoginForm()
    
    return render(request, "shea/ambulance_driver_login.html", {"form": form})

# 🚑 DASHBOARD VIEW 🚑
def ambulance_driver_dashboard(request):
    driver_id = request.session.get("driver_id")
    if not driver_id:
        return redirect("shea:ambulance_driver_login")  # Redirect using namespace

    try:
        driver = AmbulanceDriver.objects.get(id=driver_id)
    except AmbulanceDriver.DoesNotExist:
        messages.error(request, "Invalid session. Please log in again.")
        request.session.flush()  # Clear invalid session
        return redirect("shea:ambulance_driver_login")

    return render(request, "shea/ambulance_driver_dashboard.html", {"driver": driver})

# 🚑 LOGOUT VIEW 🚑
def ambulance_driver_logout(request):
    request.session.flush()  # Securely clear session
    messages.success(request, "You have been logged out.")
    return redirect("shea:ambulance_driver_login")