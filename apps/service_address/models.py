from django.db import models
from apps.users.models import PatientUser
import uuid

class ServiceAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(PatientUser, on_delete=models.CASCADE, related_name='services_address')
    departament = models.CharField(max_length=256, default='META')
    city = models.CharField(max_length=256, default='VILLAVICENCIO')
    line_address = models.CharField(max_length=256, null=False, blank=False)
    description = models.TextField(max_length=256, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_default:
            # Desmarcar otras direcciones predeterminadas del mismo usuario
            ServiceAddress.objects.filter(patient=self.patient, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)