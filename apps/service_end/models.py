from django.db import models

class ServiceEnd(models.Model):
    inability = models.CharField(max_length=256, null=False, blank=False)
    inability_days = models.IntegerField(null=False, blank=False)
    observations = models.TextField(max_length=256, null=False, blank=False)
    cie10_code = models.CharField(max_length=50, null=False, blank=False)
    cie10_description = models.TextField(max_length=256, null=False, blank=False)