from django.db import models
from apps.users.models import DoctorUser

class Vehicle(models.Model):
    doctor_user = models.ForeignKey(DoctorUser, on_delete=models.PROTECT, related_name='vehicles')
    plate = models.CharField(max_length=50, null=False, blank=False)
    brand = models.CharField(max_length=50, null=False, blank=False)
    color = models.CharField(max_length=50, null=False, blank=False)
    is_default = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.is_default:
            Vehicle.objects.filter(doctor_user=self.doctor_user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.plate} - {self.brand} - {self.color}'