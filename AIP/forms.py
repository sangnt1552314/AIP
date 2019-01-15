import os
from django import forms
from django.core import validators

def checkImageSize(value):
    if value.size > 3145728:
        raise forms.ValidationError("Image size cannot be greater than 3MB")

class Upload(forms.Form):
    image = forms.ImageField(validators=[checkImageSize, ])

    def clean(self):
        all_clean_data = super().clean()
        image = all_clean_data['image']

        if image:
            if not image.name.lower().endswith(('.png', '.jpg')):
                raise forms.ValidationError("Only accept .png and .jpg file")
