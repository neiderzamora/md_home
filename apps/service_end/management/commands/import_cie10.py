import pandas as pd
from django.core.management.base import BaseCommand
from django.db import connection
from apps.service_end.models import CIE10Code

class Command(BaseCommand):
    help = 'Importa códigos CIE-10 desde un archivo XLSX'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Ruta al archivo XLSX de CIE-10')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        
        # Verificar si la tabla existe
        with connection.cursor() as cursor:
            tables = connection.introspection.table_names()
            if 'service_end_cie10code' not in tables:
                self.stderr.write(self.style.ERROR('La tabla service_end_cie10code no existe. Ejecuta las migraciones primero.'))
                return

        try:
            self.stdout.write(self.style.WARNING(f'Leyendo archivo: {file_path}'))
            df = pd.read_excel(file_path)
            
            # Verificar las columnas
            if 'cie10_code' not in df.columns or 'cie10_description' not in df.columns:
                self.stderr.write(self.style.ERROR(f'Columnas requeridas no encontradas. Columnas disponibles: {df.columns.tolist()}'))
                return
            
            total_rows = len(df)
            created_count = 0
            updated_count = 0
            
            for index, row in df.iterrows():
                code = str(row['cie10_code']).strip()
                description = str(row['cie10_description']).strip()
                
                if code and description:
                    obj, created = CIE10Code.objects.update_or_create(
                        code=code,
                        defaults={'description': description}
                    )
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                
                if (index + 1) % 100 == 0:
                    self.stdout.write(self.style.WARNING(f'Procesados {index + 1} de {total_rows} registros'))
            
            self.stdout.write(self.style.SUCCESS(
                f'Importación completada: {created_count} creados, {updated_count} actualizados'
            ))
            
        except Exception as e:
            import traceback
            self.stderr.write(self.style.ERROR(f'Error: {str(e)}'))
            self.stderr.write(self.style.ERROR(traceback.format_exc()))