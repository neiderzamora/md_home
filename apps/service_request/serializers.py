from rest_framework import serializers
import django_filters
from apps.service_request.models import PatientServiceRequest, DoctorServiceResponse, ServiceRequestDetail
from apps.service_end.models import ServiceEnd
from apps.users.models import PatientUser, DoctorUser
from apps.users.serializers import PatientUserSerializer, DoctorUserSerializer
from apps.service_address.models import ServiceAddress
from apps.service_address.serializers import ServiceAddressSerializer

class ServiceEndSerializer(serializers.ModelSerializer):
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = ServiceEnd
        fields = '__all__'
        read_only_fields = ['end_time', 'service_request']

class PatientServiceRequestSerializer(serializers.ModelSerializer):
    patient = PatientUserSerializer(read_only=True)
    service_end = ServiceEndSerializer(read_only=True)
    location = serializers.PrimaryKeyRelatedField(queryset=ServiceAddress.objects.all())
    location_detail = ServiceAddressSerializer(source='location', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    created_at_gte = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', input_formats=['%d/%m/%Y'])
    created_at_lte = django_filters.DateFilter(field_name='created_at', lookup_expr='lte', input_formats=['%d/%m/%Y'])

    class Meta:
        model = PatientServiceRequest
        fields = '__all__'
        
class DoctorServiceResponseSerializer(serializers.ModelSerializer):
    doctor = DoctorUserSerializer()
    service_request = PatientServiceRequestSerializer()
    #service_end = ServiceEndSerializer()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    created_at_gte = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', input_formats=['%d/%m/%Y'])
    created_at_lte = django_filters.DateFilter(field_name='created_at', lookup_expr='lte', input_formats=['%d/%m/%Y'])

    class Meta:
        model = DoctorServiceResponse
        fields = '__all__'

class DoctorServiceResponseCreateSerializer(serializers.ModelSerializer):
    doctor_latitude = serializers.FloatField(write_only=True)
    doctor_longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = DoctorServiceResponse
        fields = ['doctor_latitude', 'doctor_longitude']
        
class ServiceRequestDetailSerializer(serializers.ModelSerializer):
    patient_service_request = PatientServiceRequestSerializer()
    doctor_service_response = DoctorServiceResponseSerializer()
    service_end = ServiceEndSerializer()
    location = ServiceAddressSerializer()
    patient = PatientUserSerializer()
    doctor = DoctorUserSerializer()

    class Meta:
        model = ServiceRequestDetail
        fields = '__all__'