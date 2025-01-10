import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.db import models

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

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True
    )

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

class PatientUser(User):
    IDENTIFICATION_TYPE = [
        ('CC', 'CEDULA DE CIUDADANIA'),
        ('PS', 'PASAPORTE'),
        ('CE', 'CEDULA DE EXTRANJERIA'),
    ]
    
    GENDER_TYPE = [
        ('MASCULINO', 'MASCULINO'),
        ('FEMENINO', 'FEMENINO'),
        ('O', 'OTRO')
    ]
    
    identification_type = models.CharField(max_length=30, choices=IDENTIFICATION_TYPE, default='CC')
    identification_number = models.CharField(max_length=20, null=False, blank=False)
    gender = models.CharField(max_length=30, choices=GENDER_TYPE, default='MASCULINO')
    birthdate = models.DateField()
    phone_number = models.CharField(max_length=50, unique=True, null=False, blank=False)
    address_departament = models.CharField(max_length=256, default='META')
    address_city = models.CharField(max_length=256, default='VILLAVICENCIO')
    address_line = models.CharField(max_length=256, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
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

    class Meta:
        permissions = [
            ('can_edit_patientuser', 'Can edit patient user'),
        ]
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        patient_group, created = Group.objects.get_or_create(name='Patients')
        self.groups.add(patient_group)

class DoctorUser(User):
    IDENTIFICATION_TYPE = [
        ('CC', 'CEDULA DE CIUDADANIA'),
        ('PS', 'PASAPORTE'),
        ('CE', 'CEDULA DE EXTRANJERIA'),
    ]

    GENDER_TYPE = [
        ('M', 'MASCULINO'),
        ('F', 'FEMENINO'),
        ('O', 'OTRO')
    ]    
    
    identification_type = models.CharField(max_length=30, choices=IDENTIFICATION_TYPE, default='CC')
    identification_number = models.CharField(max_length=20, null=False, blank=False)
    gender = models.CharField(max_length=30, choices=GENDER_TYPE, default='M')
    birthdate = models.DateField()
    phone_number = models.CharField(max_length=50, unique=True, null=False, blank=False)
    address_departament = models.CharField(max_length=256, default='META')
    address_city = models.CharField(max_length=256, default='VILLAVICENCIO')
    address_line = models.CharField(max_length=256, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    DOCTOR_TYPE = [
        ('MG', 'MEDICO GENERAL'),
        ('MS', 'MEDICO ESPECIALISTA'),
        ('TP', 'TERAPEUTA'),
        ('EF', 'ENFERMERA')
    ]
    rethus = models.CharField(max_length=255, null=False, blank=False, unique=True)
    doctor_type = models.CharField(max_length=50, choices=DOCTOR_TYPE)
    specialty = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        permissions = [
            ('can_edit_doctoruser', 'Can edit doctor user'),
        ]
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        patient_group, created = Group.objects.get_or_create(name='Doctors')
        self.groups.add(patient_group)