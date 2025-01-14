# Generated by Django 5.1.2 on 2025-01-03 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctoruser',
            name='gender',
            field=models.CharField(choices=[('M', 'MASCULINO'), ('F', 'FEMENINO'), ('O', 'OTRO')], default='M', max_length=30),
        ),
        migrations.AddField(
            model_name='patientuser',
            name='gender',
            field=models.CharField(choices=[('M', 'MASCULINO'), ('F', 'FEMENINO'), ('O', 'OTRO')], default='M', max_length=30),
        ),
    ]
