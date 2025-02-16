from inspect import classify_class_attrs
from symtable import Class

from django import forms
from django.core import validators
from .models import Books, Order, BookImage

from django.contrib.auth.models import Group

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class BookForm(forms.ModelForm):
    images =  MultipleFileField(label='Select files', required=False)
    class Meta:
        model = Books
        fields = 'name', 'price', 'description','discount', 'preview'
    """
    позволяем загрузить сразу несколько изображений
    """


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'user', 'delivery_address', 'promocode', 'books'


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = 'name',

class CSVImportForm(forms.Form):
    csv_file = forms.FileField()

