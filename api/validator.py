from django.core.exceptions import ValidationError

def validate_image_size(image):
    max_size = 7*1024*1024
    if image.size > max_size:
        raise ValidationError("Image file is larger than 10MB")