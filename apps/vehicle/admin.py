from django.contrib import admin
from .models import Vehicle

class VehicleAdmin(admin.ModelAdmin):
    list_display = ['id', 'doctor_user', 'plate', 'brand', 'color']
    search_fields = ['plate', 'brand', 'color']
    readonly_fields = ['id']

admin.site.register(Vehicle, VehicleAdmin)