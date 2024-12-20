from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class SuperUserHDHome(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='superuser_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='superuser_permissions',
        blank=True
    )

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

class BaseUserHDHome(AbstractBaseUser, PermissionsMixin):
    IDENTIFICATION_TYPE = [
        ('CC', 'CEDULA DE CIUDADANIA'),
        ('PS', 'PASAPORTE'),
        ('CE', 'CEDULA DE EXTRANJERIA'),
    ]
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    identification_type = models.CharField(max_length=30, choices=IDENTIFICATION_TYPE, default='CC')
    identification_number = models.CharField(max_length=20, null=False, blank=False)
    birthdate = models.DateField()
    phone_number = models.CharField(max_length=50, unique=True, null=False, blank=False)
    address_departament = models.CharField(max_length=256, default='META')
    address_city = models.CharField(max_length=256, default='VILLAVICENCIO')
    address_line = models.CharField(max_length=256, null=False, blank=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        abstract = True

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

class PatientUser(BaseUserHDHome):
    EPS_LIST = [
        ('EPS1', 'EPS1'),
        ('EPS2', 'EPS2'),
        ('EPS3', 'EPS3')
    ]
    
    PREPAID_LIST = [
        ('PREPAID1', 'PREPAID1'),
        ('PREPAID2', 'PREPAID2'),
        ('PREPAID3', 'PREPAID3')
    ]
    
    eps = models.CharField(max_length=100, choices=EPS_LIST)
    prepaid_medicine = models.CharField(max_length=100, choices=PREPAID_LIST)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='patientuser_groups',  # Agrega related_name único
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='patientuser_permissions',  # Agrega related_name único
        blank=True
    )
    
class DoctorUser(BaseUserHDHome):
    DOCTOR_TYPE = [
        ('MG', 'MEDICO GENERAL'),
        ('MS', 'MEDICO ESPECIALISTA'),
        ('TP', 'TERAPEUTA'),
        ('EF', 'ENFERMERA')
        
    ]
    rethus = models.CharField(max_length=256, null=False, blank=False, unique=True)
    doctor_type = models.CharField(max_length=50, choices=DOCTOR_TYPE)
    specialty = models.CharField(max_length=100, null=True, blank=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='doctoruser_groups',  # Agrega related_name único
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='doctoruser_permissions',  # Agrega related_name único
        blank=True
    )