# apps/users/management/commands/create_doctoruser.py

import os
from django.core.management.base import BaseCommand
from apps.users.models import DoctorUser
from datetime import datetime
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Crea un usuario tipo Doctor con credenciales predefinidas.'

    def handle(self, *args, **kwargs):
        email = 'doctor1@doctor.com'
        password = 'A1s2222222+@'
        first_name = 'miguel'
        last_name = 'fernadez'
        identification_number = '122001144'
        birthdate_str = '12/12/2000'
        phone_number = '3227110692'
        address_line = 'calle 12'
        rethus = '3232414'
        doctor_type = 'MG'

        # Convertir la fecha de nacimiento al formato YYYY-MM-DD
        try:
            birthdate = datetime.strptime(birthdate_str, '%d/%m/%Y').date()
        except ValueError:
            self.stderr.write(self.style.ERROR('Formato de fecha de nacimiento inválido. Usa DD/MM/YYYY.'))
            return

        if DoctorUser.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'El usuario con email {email} ya existe.'))
        else:
            try:
                doctor = DoctorUser.objects.create(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    identification_number=identification_number,
                    birthdate=birthdate,
                    phone_number=phone_number,
                    address_line=address_line,
                    rethus=rethus,
                    doctor_type=doctor_type
                )
                doctor.set_password(password)
                doctor.save()
                self.stdout.write(self.style.SUCCESS(f'Doctor creado exitosamente: {email}'))
            except IntegrityError as e:
                self.stderr.write(self.style.ERROR(f'Error al crear el doctor: {e}'))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Ocurrió un error inesperado: {e}'))