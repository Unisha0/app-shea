from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from hospital.models import Hospitaldb
class AmbulanceDriver(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    license_number = models.CharField(max_length=5)
    hospital = models.ForeignKey('hospital.Hospitaldb', on_delete=models.CASCADE)  # Assuming there is a Hospital model
    password = models.CharField(max_length=255 , default="null")  # To store the hashed password

    def set_password(self, raw_password):
        """Sets the password after hashing it"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Checks if the provided password matches the stored hashed password"""
        return check_password(raw_password, self.password)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
        verbose_name = "Ambulance Driver"
        verbose_name_plural = "Ambulance Drivers"

from django.db import models
from hospital.models import Hospitaldb  # Ensure correct import

# ✅ Define function BEFORE the Ambulance model
def get_default_hospital():
    hospital = Hospitaldb.objects.first()
    return hospital.id if hospital else None  # Ensuring None if no hospital exists

class Ambulance(models.Model):
    driver = models.ForeignKey('shea.AmbulanceDriver', on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospitaldb, on_delete=models.SET_NULL, null=True, blank=True, default=get_default_hospital)
    is_available = models.BooleanField(default=True)
    registration_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.registration_number} - {self.hospital.name if self.hospital else 'No Hospital Assigned'}"