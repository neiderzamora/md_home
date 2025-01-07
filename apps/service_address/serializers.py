from rest_framework import serializers
from apps.service_address.models import ServiceAddress

class ServiceAddressSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = ServiceAddress
        fields = '__all__'
        read_only_fields = ['patient', 'created_at']

    def validate(self, data):
        if data.get('is_default', False):
            # Asegurarse de que solo una dirección sea predeterminada por usuario
            ServiceAddress.objects.filter(patient=self.context['request'].user, is_default=True).update(is_default=False)
        return data