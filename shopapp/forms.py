from django.contrib.auth.models import Group
from django import forms
from .models import Product, Order

# from django.core import validators


# class ProductForm(forms.Form):
#     name = forms.CharField(label='Name', max_length=100)
#     price = forms.DecimalField(label='Price', min_value=1, max_value=100000, decimal_places=2)
#     description = forms.CharField(
#         label='Product description', 
#         widget=forms.Textarea(attrs={
#             'rows': '5',
#             'cols': '50',
#         }), 
#         validators=[validators.RegexValidator(
#             regex=r'great',
#             message='Field must contain word "great"',
#             )],
#         )

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = 'name',


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'price', 'description', 'discount', 'preview'
    
    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True,})
        )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'products', 'delivery_address', 'promocode', 'user'


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()