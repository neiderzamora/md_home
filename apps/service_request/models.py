from django.db import models
from apps.users.models import PatientUser, DoctorUser
from apps.service_address.models import ServiceAddress
import uuid

class PatientServiceRequest(models.Model):
    TYPE_PAYMENT = [
        ('EF', 'EFECTIVO'),
        ('TR', 'TRANSFERENCIA'),
    ]
    
    STATUS = [
        ('PD', 'PENDIENTE'),
        ('AC', 'ACEPTADA'),
        ('LG', 'LLEGUE'),
        ('CP', 'COMPLETADA')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(PatientUser, on_delete=models.CASCADE, related_name='service_requests')
    location = models.ForeignKey(ServiceAddress, on_delete=models.CASCADE, related_name='service_requests')
    symptoms = models.CharField(max_length=256, null=False, blank=False)
    type_payment = models.CharField(max_length=30, choices=TYPE_PAYMENT)
    status = models.CharField(max_length=20, choices=STATUS, default='PD')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request {self.id} by {self.patient}"
    
class DoctorServiceResponse(models.Model):
    STATUS = [
        ('AC', 'ACEPTADA'),
        ('RZ', 'RECHAZADA'),
        ('LG', 'LLEGUE'),
        ('CP', 'COMPLETADA')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_request = models.OneToOneField(PatientServiceRequest, on_delete=models.CASCADE, related_name='response')
    doctor = models.ForeignKey(DoctorUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='service_responses')
    status = models.CharField(max_length=20, choices=STATUS, default='AC')
    doctor_latitude = models.FloatField(null=True, blank=True)
    doctor_longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response {self.id} by {self.doctor}"