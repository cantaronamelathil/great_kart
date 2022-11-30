# from email.policy import default
# from itertools import product
# from typing_extensions import Self
# from pyexpat import model
from django.db import models

from store.models import Product,Variation
from accounts.models import Accounts


# Create your models here.
class Cart(models.Model):
    cart_id= models.CharField(max_length=250,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    
    
    def __str__(self):
        return self.cart_id

class Cartitem(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, null=True )
    quantity = models.IntegerField()
    is_activate= models.BooleanField(default=True)
    
    
    def sub_total(self):
        return self.product.price * self.quantity
    
    
    def __unicode__(self):
        return self.product
class wishlist(models.Model):
    Product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(Accounts,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)