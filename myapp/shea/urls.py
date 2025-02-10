from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.ambulance_driver_signup, name='ambulance_driver_signup'),
    path('login/', views.ambulance_driver_login, name='ambulance_driver_login'),
    path('logout/', views.ambulance_driver_logout, name='ambulance_driver_logout'),
    path('dashboard/', views.ambulance_driver_dashboard, name='ambulance_driver_dashboard'),
    # Add any other necessary routes
]
