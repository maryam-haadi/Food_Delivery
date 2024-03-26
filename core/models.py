from django.db import models
from account.models import Owner

# Create your models here.

class FoodCategory(models.Model):
    category_name = models.CharField(max_length=200)
    category_desc = models.CharField(max_length=200,blank=True)




class Restaurant(models.Model):

    category_list = [
        ("iranian","iranian"),
        ("fastfood","fastfood"),
        ("kebab","kebab"),
        ("piza","piza"),
        ("burger","burger"),
        ("sandwich","sandwich"),
        ("fried","fried"),
        ("pasta","pasta"),
        ("salad","salad"),
        ("marine","marine"),
        ("International","International"),
        ("Gilani","Gilani")
    ]


    image = models.ImageField(upload_to='images/',blank=True,null=True)
    owner = models.OneToOneField('account.Owner',on_delete=models.CASCADE,related_name='restaurant',blank=True)
    category = models.CharField(max_length=255,choices=category_list)
    delivery_time = models.CharField(max_length=80,blank=False)
    min_cart_price = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    delivery_price = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    name = models.CharField(max_length=200,blank=False)
    phone_number = models.CharField(max_length=50,blank=True)
    open_time = models.TimeField(blank=False)
    close_time = models.TimeField(blank=False)
    address_name = models.CharField(max_length=200,default='')
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)


class Favorite(models.Model):
    user =models.ForeignKey('account.User',on_delete=models.CASCADE,related_name='favorites',blank=True)
    restaurant = models.ForeignKey('core.Restaurant',on_delete=models.CASCADE,related_name='favs',blank=True,null=True)

    class Meta:
        unique_together=('user','restaurant')

class Menu(models.Model):
    restaurant =models.ForeignKey('Restaurant',on_delete=models.CASCADE,related_name='menu',blank=True)
    description =models.TextField()

    class Meta:
        unique_together=('restaurant',)



class Food(models.Model):
    menu=models.ForeignKey('Menu',on_delete=models.CASCADE,related_name='foods')
    image = models.ImageField(upload_to='images/',blank=True,null=True)
    food_category = models.ForeignKey('FoodCategory',on_delete=models.CASCADE,related_name='food',blank=False)
    name = models.CharField(max_length=150,blank=False)
    desc = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
    restaurant = models.ForeignKey('Restaurant',on_delete=models.CASCADE,related_name='resfoods')





# class Cart(models.Model):
#     user = models.ForeignKey('account.User',on_delete=models.CASCADE,related_name='carts')
#     created_at = models.DateTimeField(auto_now_add=True)
#
# class CartItem(models.Model):
#     cart = models.ForeignKey('Cart',on_delete=models.CASCADE,related_name='items')
#     food = models.ForeignKey('Food',on_delete=models.CASCADE,related_name='carts')
#     quantity = models.IntegerField()
#
#
# class Order(models.Model):
#
#     choice_list = [
#         ('pending','Pending'),
#         ('accepted','Accepted'),
#         ('preparing','Preparing'),
#         ('on_the_way','On_the_way'),
#         ('delivered','delivered'),
#         ('canceled','Canceled')
#     ]
#
#
#
#     user = models.ForeignKey('account.User',on_delete=models.CASCADE,related_name='orders')
#     restaurant = models.ForeignKey('Restaurant',on_delete=models.CASCADE,related_name='resorders')
#     total_price = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
#     status = models.CharField(max_length=255,choices=choice_list)
#     order_datetime = models.DateTimeField(auto_now_add=True)
#     delivery_address = models.ForeignKey('account.Address',on_delete=models.CASCADE,blank=True,null=True)
#
#
# class OrderItem(models.Model):
#     order = models.ForeignKey('Order',on_delete=models.CASCADE,related_name='items')
#     food = models.ForeignKey('Food',on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     price = models.DecimalField(max_digits=6,decimal_places=2,blank=False)






# class Cofe(models.Model):
#     image = models.ImageField(upload_to='images/', blank=True)
#     owner = models.OneToOneField('account.Owner', on_delete=models.CASCADE, related_name='cofe', blank=False)
#     delivery_time = models.CharField(max_length=80, blank=False)
#     min_cart_price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
#     delivery_price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
#     name = models.CharField(max_length=200, blank=False)
#     phone_number = models.CharField(max_length=50, blank=True)
#     open_time = models.TimeField(blank=False)
#     close_time = models.TimeField(blank=False)
#     is_favorite = models.BooleanField(default=False, blank=True)
#     address = models.OneToOneField('account.Address', on_delete=models.PROTECT, blank=False)




# class CofeFood(models.Model):
#     image = models.ImageField(upload_to='images/',blank=True)
#     food_category = models.ForeignKey('FoodCategory',on_delete=models.CASCADE,related_name='foods',blank=False)
#     name = models.CharField(max_length=150,blank=False)
#     desc = models.TextField(blank=True)
#     price = models.DecimalField(max_digits=6,decimal_places=2,blank=False)
#     cofe = models.ForeignKey('Cofe',on_delete=models.CASCADE,related_name='coffoods')










