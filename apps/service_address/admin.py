from django.contrib import admin
from apps.service_address.models import ServiceAddress

class ServiceAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'departament', 'city', 'line_address', 'neighborhood', 'description', 'is_default')
    list_display_links = ('id', 'patient')
    search_fields = ('patient', 'departament', 'city', 'line_address', 'description')
    list_filter = ('is_default',)
    list_per_page = 20

admin.site.register(ServiceAddress, ServiceAddressAdmin)