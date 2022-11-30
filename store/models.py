from email.policy import default
from enum import unique
from itertools import product
from tkinter import CASCADE
# from sre_constants import CATEGORY
# from unicodedata import category
from django.db import models
# from category.models import Category
from category.models import Category
# Create your models here.
from django.urls import reverse
# from offer.models import ProductOffer
# from django.forms import  ProductOfferForm
# from offer.forms import  ProductOfferForm
class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    offer     = models.IntegerField(verbose_name = "offer price",null=True,blank=True)
    
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])
    
    
    def __str__(self):
        return self.product_name
    
    @property
    def offer_percetage(self):
        return int(((self.price - self.offer)/ self.price) * 100) 
    
    # def Offer_Price(self):
    #         #  ProductOfferForm()
    #     # self.productoffer.is_valid:
        
    #         offer_price = (self.price * self.productoffer.discount) / 100
    #         new_price = self.price - offer_price
    #         return {
    #             "new_price": new_price,
    #             "discount": self.productoffer.discount,
    #         }   
    #         # return {"new_price":self.price}    

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

variation_category_choice = {
        ('color','Color'),
        ('size','size'),
    }
    
class Variation(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100,choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active   = models.BooleanField(default=True)  
    created_date = models.DateTimeField(auto_now = True)
    color_name = models.CharField(max_length=20,null=True,blank=True)
    objects = VariationManager()
    
    def __str__(self):
        return self.variation_value

    
    # def __unicode__(self):
    #     return self.product  
    
    
    
    
    
