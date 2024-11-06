from rest_framework import serializers
from apps.users.models import PatientUser, DoctorUser
from .validators import validator_password, validate_names, validate_identification, validate_birthdate, validate_phone_number

class PatientUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(validators=[validate_names])
    last_name = serializers.CharField(validators=[validate_names])
    identification_number = serializers.CharField(validators=[validate_identification])
    birthdate = serializers.DateField(
        validators=[validate_birthdate],
        format="%d/%m/%Y",
        input_formats=["%d/%m/%Y"]
    )
    phone_number = serializers.CharField(validators=[validate_phone_number])
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, validators=[validator_password])
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    created_at = serializers.DateTimeField(format='%Y-%m-%e %H:%M', read_only=True)
    
    class Meta:
        model = PatientUser
        fields = '__all__'
        
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data

    def create(self, validated_data):
        # Elimina el campo 'password2' de validated_data
        validated_data.pop('password2')

        # Crea el usuario utilizando **validated_data para pasar todos los campos automáticamente
        user = PatientUser.objects.create_user(**validated_data)

        # Establece la contraseña
        user.set_password(validated_data['password']) 
        user.save()

        return user

class DoctorUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(validators=[validate_names])
    last_name = serializers.CharField(validators=[validate_names])
    identification_number = serializers.CharField(validators=[validate_identification])
    birthdate = serializers.DateField(
        validators=[validate_birthdate],
        format="%d/%m/%Y",
        input_formats=["%d/%m/%Y"]
    )
    phone_number = serializers.CharField(validators=[validate_phone_number])
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, validators=[validator_password])
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    created_at = serializers.DateTimeField(format='%Y-%m-%e %H:%M', read_only=True)
    
    class Meta:
        model = DoctorUser
        fields = '__all__'

    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data

    def create(self, validated_data):
        # Elimina el campo 'password2' de validated_data
        validated_data.pop('password2')

        # Crea el usuario utilizando **validated_data para pasar todos los campos automáticamente
        user = DoctorUser.objects.create_user(**validated_data)

        # Establece la contraseña
        user.set_password(validated_data['password']) 
        user.save()

        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()