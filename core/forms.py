from django import forms
from .models import *

class SalespersonForm(forms.ModelForm):
    class Meta:
        model = Salesperson
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'