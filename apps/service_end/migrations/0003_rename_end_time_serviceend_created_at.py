# Generated by Django 5.1.2 on 2025-01-31 04:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service_end', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='serviceend',
            old_name='end_time',
            new_name='created_at',
        ),
    ]
