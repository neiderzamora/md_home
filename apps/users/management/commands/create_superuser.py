import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Crea un superusuario con credenciales predefinidas.'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        email = os.environ.get('SUPERUSER_EMAIL', 'admin1@admin.com')
        password = os.environ.get('SUPERUSER_PASSWORD', 'admin')
        first_name = os.environ.get('SUPERUSER_FIRST_NAME', 'admin')
        last_name = os.environ.get('SUPERUSER_LAST_NAME', 'admin')

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'El superusuario con email {email} ya existe.'))
        else:
            try:
                superuser = User.objects.create_superuser(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                superuser.is_staff = True
                superuser.is_superuser = True
                superuser.save()
                self.stdout.write(self.style.SUCCESS(f'Superusuario creado exitosamente: {email}'))
            except IntegrityError as e:
                self.stderr.write(self.style.ERROR(f'Error al crear el superusuario: {e}'))