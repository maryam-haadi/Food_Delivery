from django.db import models
from account.models import Address,Owner

# Create your models here.

class FoodCategory(models.Model):
    category_name = models.CharField(max_length=200)
    category_desc = models.CharField(max_length=255,blank=True)

class RestaurantCategory(models.Model):
    category_name = models.CharField(max_length=200)
    category_desc = models.CharField(max_length=255,blank=True)


class Restaurant(models.Model):
    image = models.ImageField(upload_to='images/',blank=True)
    owner = models.OneToOneField('account.Owner',on_delete=models.CASCADE,related_name='restaurant',blank=False)
    category = models.ForeignKey('RestaurantCategory',on_delete=models.CASCADE,related_name='restaurants',blank=False)
    delivery_time = models.CharField(max_length=80,blank=False)
    min_cart_price = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    delivery_price = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    name = models.CharField(max_length=200,blank=False)
    phone_number = models.CharField(max_length=50,blank=True)
    open_time = models.TimeField(blank=False)
    close_time = models.TimeField(blank=False)
    is_favorite = models.BooleanField(default= False,blank=True)
    address = models.OneToOneField('account.Address',on_delete=models.PROTECT,blank=False)



class RestaurantFood(models.Model):
    image = models.ImageField(upload_to='images/',blank=True)
    food_category = models.ForeignKey('FoodCategory',on_delete=models.CASCADE,related_name='food',blank=False)
    name = models.CharField(max_length=150,blank=False)
    desc = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    restaurant = models.ForeignKey('Restaurant',on_delete=models.CASCADE,related_name='resfoods')


class Cofe(models.Model):
    image = models.ImageField(upload_to='images/', blank=True)
    owner = models.OneToOneField('account.Owner', on_delete=models.CASCADE, related_name='cofe', blank=False)
    delivery_time = models.CharField(max_length=80, blank=False)
    min_cart_price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    delivery_price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    name = models.CharField(max_length=200, blank=False)
    phone_number = models.CharField(max_length=50, blank=True)
    open_time = models.TimeField(blank=False)
    close_time = models.TimeField(blank=False)
    is_favorite = models.BooleanField(default=False, blank=True)
    address = models.OneToOneField('account.Address', on_delete=models.PROTECT, blank=False)




class CofeFood(models.Model):
    image = models.ImageField(upload_to='images/',blank=True)
    food_category = models.ForeignKey('FoodCategory',on_delete=models.CASCADE,related_name='foods',blank=False)
    name = models.CharField(max_length=150,blank=False)
    desc = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    cofe = models.ForeignKey('Cofe',on_delete=models.CASCADE,related_name='coffoods')










