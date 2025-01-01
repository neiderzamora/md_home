from django.db import models
from apps.service_request.models import PatientServiceRequest
import uuid

class ServiceEnd(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_request = models.OneToOneField('service_request.PatientServiceRequest', on_delete=models.CASCADE, related_name='service_end')
    end_time = models.DateTimeField(auto_now_add=True)
    inability = models.CharField(max_length=256, null=False, blank=False)
    inability_days = models.IntegerField(null=False, blank=False)
    observations = models.TextField(max_length=256, null=False, blank=False)
    cie10_code = models.CharField(max_length=50, null=False, blank=False)
    cie10_description = models.TextField(max_length=256, null=False, blank=False)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.service_request.status = 'COMPLETADA'
        self.service_request.save()

    def __str__(self):
        return f"Service End {self.id} for Request {self.service_request.id}"