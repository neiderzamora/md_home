from django.db import models
import uuid

class BaseUserHDHome(models.Model):
    IDENTIFICATION_TYPE = [
        ('CC', 'Cédula de ciudadania'),
        ('PS', 'Pasaporte'),
        ('CE', 'Cédula de extranjería'),
    ]
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    identification_type = models.CharField(max_length=30, choices=IDENTIFICATION_TYPE, default='CC')
    identification_number = models.CharField(max_length=20, null=False, blank=False)
    birthdate = models.DateField(null=False, blank=False)
    phone_number = models.CharField(max_length=50, unique=True, null=False, blank=False)
    address_departament = models.CharField(max_length=256, default='META')
    address_city = models.CharField(max_length=256, default='VILLAVICENCIO')
    address_line = models.CharField(max_length=256, null=False, blank=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    class Meta:
        abstract = True