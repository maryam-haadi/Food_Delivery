from django.db import models
from account.models import Customer
from core.models import Food,Restaurant
# Create your models here.


class Restaurant_cart(models.Model):
    customer = models.ForeignKey('account.Customer',on_delete=models.CASCADE,related_name='cart')
    restaurant = models.ForeignKey('core.Restaurant',on_delete=models.CASCADE,related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_compelete = models.BooleanField(default=False,blank=True)


    def __str__(self):
        return self.restaurant.name




class Restaurant_cart_item(models.Model):
    restaurant_cart = models.ForeignKey('Restaurant_cart',on_delete=models.CASCADE,related_name='cart_items',blank=True,null=True)
    food = models.ForeignKey('core.Food',on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1,blank=True,null=True)


    def __str__(self):
        return f"food:{self.food.name} from restaurant:{self.restaurant_cart.restaurant.name}"


class Order(models.Model):
    restaurant_cart = models.OneToOneField('Restaurant_cart',on_delete=models.CASCADE)
    delivery_address_name = models.CharField(max_length=200,blank=True,null=True)
    latitude = models.FloatField(blank=True,null=True)
    longitude = models.FloatField(blank=True,null=True)
    total_price = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    total_price_after_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False,blank=True)
    owner_approval = models.BooleanField(default=False,blank=True)
    is_compelete = models.BooleanField(default=False,blank=True)


    def __str__(self):
        return f"order id:{self.id}   order customer:{self.restaurant_cart.customer.user.phone_number} - restaurant:{self.restaurant_cart.restaurant.name}"



    def save(self, *args, **kwargs):

        cart = self.restaurant_cart
        items = Restaurant_cart_item.objects.all().filter(restaurant_cart=cart).filter(restaurant_cart__customer=cart.customer)
        sum=0
        for item in items:
            sum += (item.food.price * item.quantity)
        self.total_price = sum + cart.restaurant.delivery_price
        super(Order, self).save(*args, **kwargs)

    def create(self,*args,**kwargs):

        cart = self.restaurant_cart
        items = Restaurant_cart_item.objects.all().filter(restaurant_cart=cart).filter(restaurant_cart__customer=cart.customer)
        sum=0
        for item in items:
            sum += (item.food.price * item.quantity)
        self.total_price = sum + cart.restaurant.delivery_price

        super(Order, self).create(*args, **kwargs)



class Payment(models.Model):
    order = models.ForeignKey('Order',on_delete=models.CASCADE,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    origin_card_number = models.CharField(max_length=16,blank=True)
    cvv2 = models.CharField(max_length=20,blank=True)
    daynamic_password = models.CharField(max_length=6,blank=True)
    verification = models.CharField(max_length=5,blank=True)
    expire_time = models.DateTimeField(blank=True,null=True)
    destination_card_number = models.CharField(max_length=16,default='5894631129807582',blank=True)
    is_complete = models.BooleanField(default=False,blank=True)





    class Meta:
        unique_together = ('order','origin_card_number')


    def __str__(self):
        return f"Payment {self.id} -  price : {self.order.total_price} - for order id : {self.order.id} - with customer : {self.order.restaurant_cart.customer} - from restaurant : {self.order.restaurant_cart.restaurant}"


    def save(self, *args, **kwargs):

        self.order.paid = True
        self.order.is_compelete = True
        self.order.restaurant_cart.is_compelete = True
        self.order.restaurant_cart.save()
        self.order.save()
        self.is_complete = True

        super(Payment, self).save(*args, **kwargs)






class ChanceSpining(models.Model):
    customer = models.ForeignKey('account.Customer',on_delete=models.CASCADE,blank=True)
    order = models.ForeignKey('cart.Order',on_delete=models.CASCADE,blank=True)
    percentage_discount = models.PositiveIntegerField(blank=True,null=True)
    amount_discount = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    absurd = models.PositiveIntegerField(blank=True,null=True)

    def __str__(self):
        return f"customer :{self.customer.user.phone_number} order id :{self.order.id}"



class Dice(models.Model):
    customer = models.ForeignKey('account.Customer',on_delete=models.CASCADE,blank=True)
    order = models.ForeignKey('cart.Order',on_delete=models.CASCADE,blank=True)
    dice1 = models.IntegerField(blank=True,null=True)
    dice2 = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return f"customer :{self.customer.user.phone_number} order id :{self.order.id} dice1:{self.dice1} dice2:{self.dice2}"

