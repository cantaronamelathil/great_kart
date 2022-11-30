

from django import forms
from django.db import models
from store.models import Product
from django.forms.widgets import CheckboxInput
from django.forms.widgets import TextInput
from .models import Product, Variation
from django.forms import ModelForm
class Product(forms.ModelForm):
    product_name = forms.CharField(
        required=True,
        max_length=200,
        widget=forms.TextInput(attrs={"placeholder": "product_name"}),
    )
    category  = forms.CharField(
        required=True,
        max_length=500,
        widget=forms.Textarea(attrs={"placeholder": "category"}),
    )
    price = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={"placeholder": "price"}),
    )
    # images = forms.ImageField(required=True,widget=FileInput)
    stock = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={"placeholder": "stock"}),
    )
    is_available = forms.BooleanField(
        required=True, widget=CheckboxInput(attrs={"placeholder": "Status"})
    )

    class Meta:
        model = Product
        fields = [
            "product_name",
            "category",
            "price",
            "images",
            "stock",
            "is_available",
            
        ]

    def _init_(self, *args, **kwargs):
        super(Product, self)._init_(
            *args, **kwargs
        )
        
        
class VarientForm(ModelForm):
    class Meta:
        model = Variation
        fields = [
            "product",
            "variation_category",
            "variation_value",
            "color_name",
            "is_active",
        ]
        widgets = {
            "variation_value": TextInput(attrs={"type": "color"}),
        }        