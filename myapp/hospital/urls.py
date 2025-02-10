from django.urls import path
from . import views
from .views import hospital_list

app_name = 'hospital'

urlpatterns = [
    path('signup/', views.hospital_signup, name='signup'),
    path('login/', views.hospital_login, name='login'),
    path('logout/', views.hospital_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Correct link for dashboard
    path('manage_hospital/', views.manage_hospital, name='manage_hospital'),
    path('edit_hospital/<int:pk>/', views.edit_hospital, name='edit_hospital'),
    path('manage_doctors/', views.manage_doctors, name='manage_doctors'),
    path('edit_doctor/<int:pk>/', views.edit_doctor, name='edit_doctor'),
    path('manage_doctor_schedules/', views.manage_doctor_schedules, name='manage_doctor_schedules'),
    path('edit_doctor_schedule/<int:doctor_id>/', views.edit_doctor_schedule, name='edit_doctor_schedule'),
    path('manage_ambulances/', views.manage_ambulances, name='manage_ambulances'),
    path('edit_ambulance/<int:pk>/', views.edit_ambulance, name='edit_ambulance'),
    
    path('api/hospitals/', hospital_list, name='hospital-list'),
]