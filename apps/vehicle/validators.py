from django.core.exceptions import ValidationError

def validate_plate(value):
    if len(value) > 50:
        raise ValidationError("Plate must be 50 characters or less.")

def validate_brand(value):
    if len(value) > 50:
        raise ValidationError("Brand must be 50 characters or less.")

def validate_color(value):
    if len(value) > 50:
        raise ValidationError("Color must be 50 characters or less.")
