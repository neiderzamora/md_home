from rest_framework import serializers
from .models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'doctor_user', 'plate', 'brand', 'color']

    def validate_plate(self, value):
        if len(value) > 50:
            raise serializers.ValidationError("Plate must be 50 characters or less.")
        return value

    def validate_brand(self, value):
        if len(value) > 50:
            raise serializers.ValidationError("Brand must be 50 characters or less.")
        return value

    def validate_color(self, value):
        if len(value) > 50:
            raise serializers.ValidationError("Color must be 50 characters or less.")
        return value
