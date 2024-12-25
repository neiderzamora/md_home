from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

User = get_user_model()

class Command(BaseCommand):
    help = 'Assign permissions to groups and users'

    def handle(self, *args, **kwargs):
        # Crear un grupo de doctores y asignar permisos
        doctor_group, created = Group.objects.get_or_create(name='Doctors')
        can_view_doctor = Permission.objects.get(codename='view_doctoruser')
        can_edit_doctor = Permission.objects.get(codename='can_edit_doctoruser')
        doctor_group.permissions.add(can_view_doctor, can_edit_doctor)

        # Crear un grupo de pacientes y asignar permisos
        patient_group, created = Group.objects.get_or_create(name='Patients')
        can_view_patient = Permission.objects.get(codename='view_patientuser')
        can_edit_patient = Permission.objects.get(codename='can_edit_patientuser')
        patient_group.permissions.add(can_view_patient, can_edit_patient)

        # Asignar un usuario al grupo de doctores
        """ doctor_user = User.objects.get(email='email@email.com')
        doctor_user.groups.add(Doctors) """

        # Asignar un usuario al grupo de pacientes
        """ patient_user = User.objects.get(email='patient_user@example.com')
        patient_user.groups.add(patient_group) """

        self.stdout.write(self.style.SUCCESS('Successfully assigned permissions'))