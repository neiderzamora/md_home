from rest_framework import serializers
from apps.service_end.models import ServiceEnd, CIE10Code

class CIE10CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CIE10Code
        fields = '__all__'