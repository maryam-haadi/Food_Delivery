from django.db import models
from account.models import Owner
from datetime import  timedelta, datetime

# Create your models here.

class FoodCategory(models.Model):
    category_name = models.CharField(max_length=255)

    class Meta:
        unique_together=('category_name',)

    def __str__(self):
        return self.category_name




class FoodCategoryRequest(models.Model):
    restaurant = models.ForeignKey('Restaurant',on_delete=models.CASCADE,related_name='category_request',blank=True)
    cat_name = models.CharField(max_length=255,blank=False)
    cat_desc = models.TextField(blank=True)
    admin_approval = models.BooleanField(default=False,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)


    def __str__(self):
        return self.restaurant.name





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
    is_open = models.BooleanField(default=False,blank=True)

    def save(self, *args, **kwargs):
        current_time = datetime.now().time()
        if self.open_time <= current_time < self.close_time:
            self.is_open = True
        else:
            self.is_open = False

        super(Restaurant, self).save(*args, **kwargs)

    def create(self,*args,**kwargs):
        current_time = datetime.now().time()
        if self.open_time <= current_time < self.close_time:
            self.is_open = True
        else:
            self.is_open = False
        super(Restaurant, self).create(*args, **kwargs)





class DeleteRestaurantRequest(models.Model):
    restaurant = models.ForeignKey('Restaurant',on_delete=models.CASCADE,related_name='delete_request')
    desc = models.TextField(blank=True)
    admin_approval = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.restaurant.name








class Favorite(models.Model):
    user =models.ForeignKey('account.User',on_delete=models.CASCADE,related_name='favorites',blank=True)
    restaurant = models.ForeignKey('core.Restaurant',on_delete=models.CASCADE,related_name='favs',blank=True,null=True)

    class Meta:
        unique_together=('user','restaurant')





class Menu(models.Model):
    restaurant =models.ForeignKey('Restaurant',on_delete=models.CASCADE,related_name='menu',blank=True)

    class Meta:
        unique_together=('restaurant',)



class Food(models.Model):

    menu=models.ForeignKey('Menu',on_delete=models.CASCADE,related_name='menu_foods')
    image = models.ImageField(upload_to='images/',blank=True,null=True)
    food_category = models.ForeignKey('FoodCategory',on_delete=models.CASCADE,related_name='food',blank=False)
    name = models.CharField(max_length=150,blank=False)
    desc = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,blank=False)






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






























