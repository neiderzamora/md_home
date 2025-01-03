# Generated by Django 5.1.2 on 2024-12-31 21:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('service_address', '0002_initial'),
        ('service_end', '0002_initial'),
        ('service_request', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorserviceresponse',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_responses', to='users.doctoruser'),
        ),
        migrations.AddField(
            model_name='patientservicerequest',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_requests', to='service_address.serviceaddress'),
        ),
        migrations.AddField(
            model_name='patientservicerequest',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_requests', to='users.patientuser'),
        ),
        migrations.AddField(
            model_name='doctorserviceresponse',
            name='service_request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='response', to='service_request.patientservicerequest'),
        ),
        migrations.AddField(
            model_name='servicerequestdetail',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.doctoruser'),
        ),
        migrations.AddField(
            model_name='servicerequestdetail',
            name='doctor_service_response',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='service_request_detail', to='service_request.doctorserviceresponse'),
        ),
        migrations.AddField(
            model_name='servicerequestdetail',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service_address.serviceaddress'),
        ),
        migrations.AddField(
            model_name='servicerequestdetail',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.patientuser'),
        ),
        migrations.AddField(
            model_name='servicerequestdetail',
            name='patient_service_request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='service_request_detail', to='service_request.patientservicerequest'),
        ),
        migrations.AddField(
            model_name='servicerequestdetail',
            name='service_end',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='service_request_detail', to='service_end.serviceend'),
        ),
    ]
