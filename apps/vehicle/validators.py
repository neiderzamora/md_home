from django.core.exceptions import ValidationError

def validate_plate(value):
    if len(value) < 3:
        raise ValidationError("La placa debe contener al menos 3 caracteres.")

def validate_brand(value):
    if len(value) < 3:
        raise ValidationError("La marca debe contener al menos 3 caracteres.")

def validate_color(value):
    if len(value) < 3:
        raise ValidationError("El color debe contener al menos 3 caracteres.")
