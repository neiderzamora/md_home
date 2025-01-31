from django.contrib import admin
from .models import ServiceEnd, CIE10Code

class ServiceEndAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_request', 'created_at', 'inability', 'inability_days')

class CIE10CodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code', 'description')

admin.site.register(ServiceEnd, ServiceEndAdmin)
admin.site.register(CIE10Code, CIE10CodeAdmin)    