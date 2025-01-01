from django.contrib import admin
from .models import PatientServiceRequest, DoctorServiceResponse, ServiceRequestDetail

class PatientServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'location', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['patient__first_name', 'patient__last_name']
    readonly_fields = ['id', 'created_at']

class DoctorServiceResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'service_request', 'doctor', 'created_at']
    search_fields = ['doctor__first_name', 'doctor__last_name']
    readonly_fields = ['id', 'created_at']

class ServiceRequestDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient_service_request', 'doctor_service_response', 'service_end', 'location', 'patient', 'doctor']

admin.site.register(PatientServiceRequest, PatientServiceRequestAdmin)
admin.site.register(DoctorServiceResponse, DoctorServiceResponseAdmin)
admin.site.register(ServiceRequestDetail, ServiceRequestDetailAdmin)
