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
    customer = models.ForeignKey('account.User',on_delete=models.CASCADE,related_name='orders')
    restaurant = models.ForeignKey('core.Restaurant',on_delete=models.PROTECT,related_name='res_orders')
    cart = models.OneToOneField('Restaurant_cart',on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"order customer:{self.customer.user.phone_number} - restaurant:{self.restaurant.name}"



class Payment(models.Model):
    order = models.ForeignKey('Order',on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.order.total_price}"







