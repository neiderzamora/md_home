from rest_framework import serializers
from apps.service_address.models import ServiceAddress

class ServiceAddressSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = ServiceAddress
        fields = '__all__'

    def validate(self, data):
        if data.get('is_default', False):
            # Asegurarse de que solo una dirección sea predeterminada por usuario
            ServiceAddress.objects.filter(patient=data['patient'], is_default=True).update(is_default=False)
        return data