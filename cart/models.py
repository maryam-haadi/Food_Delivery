from django.db import models
from account.models import Customer
from core.models import Food,Restaurant
# Create your models here.


class Restaurant_cart(models.Model):
    customer = models.ForeignKey('account.Customer',on_delete=models.CASCADE,related_name='cart')
    restaurant = models.ForeignKey('core.Restaurant',on_delete=models.CASCADE,related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('customer','restaurant')

    def __str__(self):
        return self.restaurant.name




class Restaurant_cart_item(models.Model):
    restaurant_cart = models.ForeignKey('Restaurant_cart',on_delete=models.CASCADE,related_name='cart_items',blank=True,null=True)
    food = models.ForeignKey('core.Food',on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1,blank=True,null=True)


    class Meta:
        unique_together = ('restaurant_cart','food')

    def __str__(self):
        return f"food:{self.food.name} from restaurant:{self.restaurant_cart.restaurant.name}"


class Order(models.Model):
    restaurant_cart = models.OneToOneField('Restaurant_cart',on_delete=models.CASCADE)
    delivery_address_name = models.CharField(max_length=200,blank=True,null=True)
    latitude = models.FloatField(blank=True,null=True)
    longitude = models.FloatField(blank=True,null=True)
    total_price = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False,blank=True)
    owner_approval = models.BooleanField(default=False,blank=True)
    is_compelete = models.BooleanField(default=False,blank=True)


    def __str__(self):
        return f"order customer:{self.restaurant_cart.customer.user.phone_number} - restaurant:{self.restaurant_cart.restaurant.name}"



class Payment(models.Model):
    order = models.ForeignKey('Order',on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.order.total_price}"







