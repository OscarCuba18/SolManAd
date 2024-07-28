from django.core.exceptions import ValidationError

def validar_mp4(value):
    if value and not value.name.endswith('.mp4'):
        raise ValidationError("El archivo de video debe ser de tipo mp4.")

def validar_img_format(value):
    if value and not value.name.endswith('.png'):
        raise ValidationError("El archivo de video debe ser de tipo png.")

# def validar_image_size(value):
#     # Validación de tamaño de archivo de imagen
#     if value and value.image.size > 5 * 1024 * 1024:
#         raise ValidationError("El tamaño de la imagen no puede exceder 5MB.")