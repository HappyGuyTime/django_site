from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
 
class UserBioForm(forms.Form):
    name = forms.CharField(label='Your Full Name' ,max_length=100)
    age = forms.IntegerField(label='Your age', min_value=1, max_value=100)
    bio = forms.CharField(label='Biography', widget=forms.Textarea)


def validate_file_max_size(file: InMemoryUploadedFile) -> None:
    max_size = 1024
    if max_size < (round(file.size / 1024, 1)):
        raise ValidationError(f"File size exceeds the maximum limit {max_size} kb")


def validate_file_name(file: InMemoryUploadedFile) -> None:
    if file.name and "virus" in file.name:
        raise ValidationError("file name should not contain `virus`")


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name, validate_file_max_size])