from django.urls import path
from . import views
from .views import patient_map

urlpatterns = [
    path('signup/', views.signup, name='patient_signup'),
    path('login/', views.login, name='patient_login'),
    path('dashboard/', views.dashboard, name='patient_dashboard'),
    path('hospital/', views.hospital, name='hospital'),
    path('ambulance/', views.ambulance, name='ambulance'),
    path('user_account/', views.user_account, name='user_account'),
    path('help/', views.help_page, name='help_page'),
    path('patient-history/', views.patient_history, name='patient_history'),
    path('logout/', views.logout, name='logout'),

      path("map/", patient_map, name="patient_map"),
    
]



