from django import forms

from . import validators


class JpegField(forms.ImageField):
    default_validators = [validators.validate_jpeg_file_extension]
