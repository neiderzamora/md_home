from django.core.validators import RegexValidator
from rest_framework import serializers
from datetime import datetime, date

def validator_password(value):
    if len(value) < 8:
        raise serializers.ValidationError("La contraseña debe exceder los 10 caracteres.")
    if not any(char.isdigit() for char in value):
        raise serializers.ValidationError("La contraseña debe contener al menos un número.")
    if not any(char.isupper() for char in value):
        raise serializers.ValidationError("La contraseña debe contener al menos una letra mayúscula.")
    if not any(char.islower() for char in value):
        raise serializers.ValidationError("La contraseña debe contener al menos una letra minúscula.")
    if not any(char in "!@#$%^&*()" for char in value):
        raise serializers.ValidationError("La contraseña debe contener al menos un carácter especial (!@#$%^&*).")
    
    return value

def validate_names(value):
    regex_validator = RegexValidator(
        regex=r'^[a-zA-Z]+$', 
        message="El nombre solo debe contener letras."
    )
    regex_validator(value)

    if len(value) < 3:
        raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
    
    return value

def validate_identification(value):
    regex_validator = RegexValidator(
        regex=r'^\d+$',
        message="La identificación solo debe contener números."
    )
    regex_validator(value)
    
    if len(value) < 5:
        raise serializers.ValidationError("La identificación debe tener al menos 5 caracteres.")
    
    return value

def validate_birthdate(value):
    today = date.today()
    
    # Cálculo de la edad
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    
    # Verifica si la persona es mayor de 18 años
    if age < 18:
        raise serializers.ValidationError("El usuario debe ser mayor de 18 años.")
    
    return value

def validate_phone_number(value):
    regex_validator = RegexValidator(
        regex=r'^\d{10}$',
        message="El número de teléfono debe contener exactamente 10 dígitos."
    )
    regex_validator(value)
    
    return value