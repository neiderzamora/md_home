from rest_framework import serializers
from .validators import validate_plate, validate_brand, validate_color
from .models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    plate = serializers.CharField(validators=[validate_plate])
    brand = serializers.CharField(validators=[validate_brand])
    color = serializers.CharField(validators=[validate_color])
    
    class Meta:
        model = Vehicle
        fields = ['id', 'plate', 'brand', 'color', 'doctor_user']
        read_only_fields = ['id', 'doctor_user']