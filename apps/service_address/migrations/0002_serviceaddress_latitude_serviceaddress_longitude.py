# Generated by Django 5.1.2 on 2025-02-06 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_address', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceaddress',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='serviceaddress',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
