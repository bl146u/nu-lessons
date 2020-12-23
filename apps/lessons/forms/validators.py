from django.core import validators


def validate_jpeg_file_extension(value):
    return validators.FileExtensionValidator(allowed_extensions=["jpg", "jpeg"])(value)
