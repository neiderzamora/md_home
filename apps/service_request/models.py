from django.db import models
from apps.users.models.models import PatientUser, DoctorUser
from apps.service_address.models import ServiceAddress
from apps.service_end.models import ServiceEnd
import uuid

class ServiceRequest(models.Model):
    TYPE_PAYMENT = [
        ('EF', 'EFECTIVO'),
        ('TR', 'TRANSFERENCIA'),
    ]
    
    STATUS = [
        ('PD', 'PENDIENTE'),
        ('AC', 'ACEPTADA'),
        ('RZ', 'RECHAZADA'),
        ('CP', 'COMPLETADA')
    ]
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    patient = models.ForeignKey(PatientUser, on_delete=models.CASCADE, related_name='services_request')
    location = models.ForeignKey(ServiceAddress, on_delete=models.CASCADE, related_name='services_request')
    doctor = models.ForeignKey(DoctorUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_requests')
    document_service_end = models.ForeignKey(ServiceEnd, on_delete=models.SET_NULL, null=True, blank=True, related_name='services_request')
    
    symptoms = models.CharField(max_length=256, null=False, blank=False)
    type_payment = models.CharField(max_length=30, choices=TYPE_PAYMENT)
    status = models.CharField(max_length=20, choices=STATUS, default='PENDIENTE')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def accept(self, doctor):
        self.status = 'ACEPTADA'
        self.doctor = doctor
        self.save()
        
    def reject(self):
        self.status = 'RECHAZADA'
        self.save()