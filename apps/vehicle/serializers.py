from rest_framework import serializers
from .validators import validate_plate, validate_brand, validate_color
from .models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    plate = serializers.CharField(validators=[validate_plate])
    brand = serializers.CharField(validators=[validate_brand])
    color = serializers.CharField(validators=[validate_color])
    
    class Meta:
        model = Vehicle
        fields = ['id', 'plate', 'brand', 'color']
        read_only_fields = ['id', 'doctor_user']
    
    def validate(self, data):
        if data.get('is_default', False):
            # Asegurarse de que solo un vehículo sea predeterminado por usuario
            Vehicle.objects.filter(doctor_user=self.context['request'].user, is_default=True).update(is_default=False)
        return data