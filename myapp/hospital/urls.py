from django.urls import path
from . import views
from .views import hospital_list

app_name = 'hospital'

urlpatterns = [
    path('signup/', views.hospital_signup, name='signup'),
    path('login/', views.hospital_login, name='login'),
    path('logout/', views.hospital_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Correct link for dashboard
    path('manage_ambulances/', views.manage_ambulances, name='manage_ambulances'),
    path('notifications/', views.notifications, name='notifications'),
    path('account_settings/', views.account_settings, name='account_settings'),
    path('help_and_support/', views.help_and_support, name='help_and_support'),
    path('api/hospitals/', hospital_list, name='hospital-list'),
]