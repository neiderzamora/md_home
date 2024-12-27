from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.users.models import DoctorUser, PatientUser
from apps.vehicle.models import Vehicle  # Asegúrate de importar el modelo Vehicle

class Command(BaseCommand):
    help = 'Assign permissions to groups and users'

    def handle(self, *args, **kwargs):
        # Crear un grupo de doctores y asignar permisos
        doctor_group, created = Group.objects.get_or_create(name='Doctors')
        doctor_content_type = ContentType.objects.get_for_model(DoctorUser)
        vehicle_content_type = ContentType.objects.get_for_model(Vehicle)

        can_view_doctor = Permission.objects.get(codename='view_doctoruser', content_type=doctor_content_type)
        can_add_doctor = Permission.objects.get(codename='add_doctoruser', content_type=doctor_content_type)
        can_change_doctor = Permission.objects.get(codename='change_doctoruser', content_type=doctor_content_type)
        can_view_vehicle = Permission.objects.get(codename='view_vehicle', content_type=vehicle_content_type)
        can_add_vehicle = Permission.objects.get(codename='add_vehicle', content_type=vehicle_content_type)
        can_change_vehicle = Permission.objects.get(codename='change_vehicle', content_type=vehicle_content_type)
        can_delete_vehicle = Permission.objects.get(codename='delete_vehicle', content_type=vehicle_content_type)

        doctor_group.permissions.add(
            can_view_doctor, can_add_doctor, can_change_doctor,
            can_view_vehicle, can_add_vehicle, can_change_vehicle, can_delete_vehicle
        )

        # Crear un grupo de pacientes y asignar permisos
        patient_group, created = Group.objects.get_or_create(name='Patients')
        patient_content_type = ContentType.objects.get_for_model(PatientUser)

        can_view_patient = Permission.objects.get(codename='view_patientuser', content_type=patient_content_type)
        can_add_patient = Permission.objects.get(codename='add_patientuser', content_type=patient_content_type)
        can_change_patient = Permission.objects.get(codename='change_patientuser', content_type=patient_content_type)

        patient_group.permissions.add(
            can_view_patient, can_add_patient, can_change_patient,
            can_view_vehicle, can_add_vehicle, can_change_vehicle, can_delete_vehicle
        )

        self.stdout.write(self.style.SUCCESS('Successfully assigned permissions'))