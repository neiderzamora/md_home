from django.contrib import admin
from .models import ServiceEnd

class ServiceEndAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_request', 'end_time', 'inability', 'inability_days', 'cie10_code', 'cie10_description')
    
admin.site.register(ServiceEnd, ServiceEndAdmin)