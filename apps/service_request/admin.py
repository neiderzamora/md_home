from django.contrib import admin
from .models import PatientServiceRequest, DoctorServiceResponse

class PatientServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'location', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['patient__first_name', 'patient__last_name']
    readonly_fields = ['id', 'created_at']

class DoctorServiceResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'service_request', 'doctor', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['doctor__first_name', 'doctor__last_name']
    readonly_fields = ['id', 'created_at']

admin.site.register(PatientServiceRequest, PatientServiceRequestAdmin)
admin.site.register(DoctorServiceResponse, DoctorServiceResponseAdmin)
