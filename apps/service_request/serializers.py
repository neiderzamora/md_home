from rest_framework import serializers
from .models import PatientServiceRequest, DoctorServiceResponse
from apps.service_end.models import ServiceEnd

class PatientServiceRequestSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = PatientServiceRequest
        fields = '__all__'

class DoctorServiceResponseSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = DoctorServiceResponse
        fields = '__all__'

class DoctorServiceResponseCreateSerializer(serializers.ModelSerializer):
    doctor_latitude = serializers.FloatField(write_only=True)
    doctor_longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = DoctorServiceResponse
        fields = ['doctor_latitude', 'doctor_longitude', 'status']

class ServiceEndSerializer(serializers.ModelSerializer):
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = ServiceEnd
        fields = '__all__'