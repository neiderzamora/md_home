import django_filters
from .models import PatientServiceRequest, DoctorServiceResponse

class PatientServiceRequestFilter(django_filters.FilterSet):
    class Meta:
        model = PatientServiceRequest
        fields = {
            'status': ['exact'],
            'created_at': ['gte', 'lte'],
        }

class DoctorServiceResponseFilter(django_filters.FilterSet):
    class Meta:
        model = DoctorServiceResponse
        fields = {
            'created_at': ['gte', 'lte'],
        }