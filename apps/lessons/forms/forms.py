from crispy_forms import helper
from crispy_forms import layout

from django import forms

from . import fields


class T74Form(forms.Form):
    image = fields.JpegField(label="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = helper.FormHelper(self)
        self.helper.form_id = "form-lesson-t74"
        self.helper.attrs = {"novalidate": "novalidate", "autocomplete": "off"}
        self.helper.layout = layout.Layout("image")
