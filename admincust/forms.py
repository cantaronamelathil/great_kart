from django import forms
from django.db import models
from coupon.models import Coupon
from django.forms.widgets import CheckboxInput
from store.models import Product
from django.forms import ModelForm
from category.models import Category
from orders. models import Order
from store.models import  Product, Variation
from django.forms.widgets import TextInput
# from offer.models import ProductOffer
class ProductForm(forms.ModelForm):
    product_name = forms.CharField(
        required=True,
        max_length=200,
        widget=forms.TextInput(attrs={"placeholder": "product_name"}),
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
    
    offer = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={"placeholder": "offer"}),
    )

    class Meta:
        model = Product
        fields = [
            "product_name",
            "category",
            "price",
            "images",
            "slug",
            # "images1",
            # "images2",
            # "images3",
            "stock",
            "is_available",
            "offer",
        ]
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ["category_name", "slug", "cat_image" ]
        
        
class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'        
            
            
            
class EditVarient(forms.ModelForm):
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

class EditCoupon(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = [
            "coupon_name",
            "code",
            "coupon_limit",
            "valid_from",
            "valid_to",
            "discount",
        ]           
        
        
        
        
class EditProductOffer(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["product_name"]
    