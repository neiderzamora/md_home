# Generated by Django 5.1.2 on 2025-01-31 03:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('service_end', '0001_initial'),
        ('service_request', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceend',
            name='service_request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='service_end', to='service_request.patientservicerequest'),
        ),
    ]
