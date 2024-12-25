from django.contrib import admin
from apps.users.models import DoctorUser, PatientUser, User

class DoctorUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = ('id', 'email')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    list_per_page = 20

class PatientUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_active')
    list_display_links = ('id', 'email')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active',)
    list_per_page = 20

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = ('id', 'email')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    list_per_page = 20

admin.site.register(DoctorUser, DoctorUserAdmin)
admin.site.register(PatientUser, PatientUserAdmin)
admin.site.register(User, UserAdmin)