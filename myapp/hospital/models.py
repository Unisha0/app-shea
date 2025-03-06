from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist


class Hospital(models.Model):
    hospital_id = models.CharField(max_length=50, unique=True , default=1)  # New unique hospital_id
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, blank = True)
    pan_number = models.CharField(max_length=9, unique=True, default="000000000")  # PAN number (9 digits)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        """Hashes the password before saving it."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Check if the provided password matches the hashed password."""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def merge_with_hospitaldb(self):
        """If a matching hospital exists in Hospitaldb, merge the information."""
        try:
            hospital_db = Hospitaldb.objects.get(name=self.name)  # Try to find a matching hospital in Hospitaldb
            # Merge the relevant fields from Hospitaldb to Hospital
            self.address = self.address or hospital_db.address  # If no address in Hospital, use from Hospitaldb
            self.website = self.website or hospital_db.contact  # If no website in Hospital, use contact from Hospitaldb
            self.description = self.description or hospital_db.speciality  # Merge speciality into description if no description
            self.save()  # Save the changes to the Hospital model
            return hospital_db  # Return the Hospitaldb object for further use or verification
        except ObjectDoesNotExist:
            return None  # Return None if no matching Hospitaldb entry is found


class Hospitaldb(models.Model):
    hospital_id = models.ForeignKey(Hospital, on_delete=models.CASCADE, default=1)  # New unique hospital_id
    name = models.CharField(max_length=255, unique=True)
    speciality = models.CharField(max_length=255)
    contact = models.CharField(max_length=50)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    email = models.EmailField(unique=True, blank = True)

    def __str__(self):
        return self.name


class Ambulance(models.Model):
    hospital = models.ForeignKey(Hospital, related_name='ambulances', on_delete=models.CASCADE)
    ambulance_number = models.CharField(max_length=20)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"Ambulance {self.ambulance_number}"
