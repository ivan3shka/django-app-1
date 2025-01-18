from django import forms
from django.core.exceptions import ValidationError
from django.core.files.storage.memory import InMemoryFileNode


class UserBioForm(forms.Form):
    name = forms.CharField(max_length=30)
    age = forms.IntegerField(label='Your age', min_value=1, max_value=100) #label -> то что будет перед формой
    bio = forms.CharField(label='Biography', widget=forms.Textarea)

def validate_file_name(file: InMemoryFileNode) -> None:
    if file.name and 'virus' in file.name:
        raise ValidationError('file can not contain "virus"')

class FileUploadForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name])


