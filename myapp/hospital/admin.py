# hospital/admin.py

from django.contrib import admin
from .models import Hospital , Hospitaldb
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'speciality', 'contact', 'address', 'latitude', 'longitude')  # Fields to display in the list view
    search_fields = ('name', 'speciality', 'contact')  # Fields to search by in the admin panel
    list_filter = ('speciality',)  # Allow filtering by speciality

admin.site.register(Hospital)
admin.site.register(Hospitaldb)