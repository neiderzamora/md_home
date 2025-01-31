from django.db import models
from apps.users.models import PatientUser, DoctorUser
from apps.service_address.models import ServiceAddress
from apps.vehicle.models import Vehicle
import uuid

class PatientServiceRequest(models.Model):
    TYPE_PAYMENT = [
        ('EFECTIVO', 'EFECTIVO'),
        ('TRANSFERENCIA', 'TRANSFERENCIA'),
    ]
    
    STATUS = [
        ('PENDIENTE', 'PENDIENTE'),
        ('ACEPTADA Y EN CAMINO', 'ACEPTADA Y EN CAMINO'),
        ('LLEGADA AL DOMICILIO', 'LLEGADA AL DOMICILIO'),
        ('COMPLETADA', 'COMPLETADA')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(PatientUser, on_delete=models.PROTECT, related_name='service_requests')
    location = models.ForeignKey(ServiceAddress, on_delete=models.PROTECT, related_name='service_requests')
    symptoms = models.CharField(max_length=256, null=False, blank=False)
    type_payment = models.CharField(max_length=30, choices=TYPE_PAYMENT)
    status = models.CharField(max_length=20, choices=STATUS, default='PENDIENTE')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request {self.id} by {self.patient}"
    
class DoctorServiceResponse(models.Model):  
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_request = models.OneToOneField(PatientServiceRequest, on_delete=models.PROTECT, related_name='response')
    doctor = models.ForeignKey(DoctorUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='service_responses')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, related_name='service_responses')
    doctor_latitude = models.FloatField(null=True, blank=True)
    doctor_longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response {self.id} by {self.doctor}"

class ServiceRequestDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_service_request = models.OneToOneField(PatientServiceRequest, on_delete=models.PROTECT, related_name='service_request_detail')
    doctor_service_response = models.OneToOneField(DoctorServiceResponse, on_delete=models.PROTECT, related_name='service_request_detail')
    service_end = models.OneToOneField('service_end.ServiceEnd', on_delete=models.PROTECT, related_name='service_request_detail')
    location = models.ForeignKey(ServiceAddress, on_delete=models.PROTECT)
    patient = models.ForeignKey(PatientUser, on_delete=models.PROTECT)
    doctor = models.ForeignKey(DoctorUser, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ServiceRequestDetail {self.id}"