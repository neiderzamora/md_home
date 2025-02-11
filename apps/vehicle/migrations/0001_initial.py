# Generated by Django 5.1.2 on 2025-01-14 03:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate', models.CharField(max_length=50)),
                ('brand', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=50)),
                ('doctor_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='users.doctoruser')),
            ],
        ),
    ]
