from django.urls import path
from . import views

app_name = 'hospital'

urlpatterns = [
    path('signup/', views.hospital_signup, name='signup'),
    path('login/', views.hospital_login, name='login'),
    path('logout/', views.hospital_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Corrected
    path('manage_ambulances/', views.manage_ambulances, name='manage_ambulances'),
    path('notifications/', views.notifications, name='notifications'),
    path('account_settings/', views.account_settings, name='account_settings'),
    path('help_and_support/', views.help_and_support, name='help_and_support'),
    
    # API to list hospitals
    path('api/hospitals/', views.hospital_list, name='hospital-list'),

    # Hospital profile (Ensure profile view exists in views.py)
    path('profile/', views.profile, name='profile'),

    # Ambulance request handling
    path('ambulance-requests/', views.view_ambulance_requests, name='view_ambulance_requests'),
    path('respond-request/<int:request_id>/<str:response>/', views.respond_to_request, name='respond_request'),
]