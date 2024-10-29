from django.db import models
from apps.users.models import DoctorUser

class Vehicle(models.Model):
    doctor_user = models.ForeignKey(DoctorUser, on_delete=models.CASCADE, related_name='vehicles')
    plate = models.CharField(max_length=50, null=False, blank=False)
    brand = models.CharField(max_length=50, null=False, blank=False)
    color = models.CharField(max_length=50, null=False, blank=False)