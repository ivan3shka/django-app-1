from django import forms
from django.core import validators
from .models import Books, Order

from django.contrib.auth.models import Group


#class BookForm(forms.Form):
#    name = forms.CharField(max_length=100)
#    price = forms.DecimalField(min_value=10, max_value=9999, decimal_places=2)
#    description = forms.CharField(label='Book description',
#                                  widget=forms.Textarea(attrs={'rows':5,
#                                                               'cols':30}),
#                                  validators=[validators.RegexValidator(
#                                      regex=r'greate',
#                                      message='Must contain word "greate"'
#                                  )])


class CreateBookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = 'name', 'price', 'description','discount'


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'user', 'delivery_address', 'promocode', 'books'


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = 'name',


