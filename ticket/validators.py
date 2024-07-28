from django.core.exceptions import ValidationError
import datetime

def validar_fecha_requerida(value):
    if value < datetime.date.today():
        raise ValidationError("La fecha requerida debe ser posterior a la fecha solicitada!")

def validar_descripcion(value):
    if len(value) < 20:
        raise ValidationError("La descripción es muy corta, debe tener al menos 100 caracteres.")