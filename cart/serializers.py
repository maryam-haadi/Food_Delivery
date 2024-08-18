from rest_framework import serializers
from .models import Restaurant_cart,Restaurant_cart_item,Order,Payment,ChanceSpining
# from core.serializers import FoodShowSerializer
from core.models import *
import random


class FoodShowSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(source='food_category.category_name',max_length=200)
    average_rating = serializers.SerializerMethodField(method_name='get_average_rating')
    class Meta:
        model = Food
        fields=['id','image','category_name','name','desc','price','average_rating']

    def get_average_rating(self,obj):
        ratings = obj.ratings.all()
        if not ratings:
            return 0
        return round(sum(rating.stars for rating in ratings)/len(ratings),2)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and instance.image:
            representation['image'] = request.build_absolute_uri(instance.image.url)
        return representation

class ResInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id','name','image']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and instance.image:
            representation['image'] = request.build_absolute_uri(instance.image.url)
        return representation




class CartShowSerializer(serializers.ModelSerializer):
    restaurant = ResInformationSerializer()
    detail = serializers.SerializerMethodField(method_name='get_detail',read_only=True)
    class Meta:
        model = Restaurant_cart
        fields =['id','restaurant','created_at','updated_at','detail','is_compelete']

    def get_detail(self,obj:Restaurant_cart):
        cart_items = Restaurant_cart_item.objects.all().filter(restaurant_cart=obj)
        food_list = []
        for item in cart_items:
            food_list.append(f"food : {item.food.name} - quantity : {item.quantity} ")
        return food_list


class CartPostSerializer(serializers.ModelSerializer):
    res_id = serializers.IntegerField(source='restaurant.id')
    class Meta:
        model = Restaurant_cart
        fields = ['res_id']


class Addcartitemserializer(serializers.ModelSerializer):
    food_id = serializers.IntegerField(source='food.pk')
    class Meta:
        model = Restaurant_cart_item
        fields = ['food_id']




class Showcartitemserializer(serializers.ModelSerializer):
    restaurant_cart = CartShowSerializer()
    food = FoodShowSerializer()
    class Meta:
        model = Restaurant_cart_item
        fields = ['id','restaurant_cart','food','quantity']


class Updatecartitemserializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant_cart_item
        fields = ['quantity']

    def validate(self, attrs):
        if attrs['quantity'] < 0:
            return serializers.ValidationError("errorrr")
        return attrs




class ShowOrderSerializer(serializers.ModelSerializer):

    delivery_price = serializers.SerializerMethodField(method_name='get_delivery_price',read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price',read_only=True)
    total_order = serializers.SerializerMethodField(method_name='get_total_order',read_only=True)
    detail = serializers.SerializerMethodField(method_name='get_details',read_only=True)
    class Meta:
        model = Order
        fields = ['id','delivery_price','total_order','total_price','delivery_address_name','latitude','longitude','detail','paid']


    def get_delivery_price(self,obj:Order):
        return obj.restaurant_cart.restaurant.delivery_price
    def get_total_order(self,obj:Order):
        sum = 0
        cart_items = Restaurant_cart_item.objects.all().filter(restaurant_cart=obj.restaurant_cart)
        for item in cart_items:
            result = item.food.price * item.quantity
            sum += result

        return sum


    def get_total_price(self,obj:Order):
        sum = 0
        cart_items = Restaurant_cart_item.objects.all().filter(restaurant_cart=obj.restaurant_cart)
        for item in cart_items:
            result = item.food.price * item.quantity
            sum += result

        sum += obj.restaurant_cart.restaurant.delivery_price
        obj.total_price = sum
        obj.save()
        return sum

    def get_details(self,obj:Order):
        cart_items = Restaurant_cart_item.objects.all().filter(restaurant_cart=obj.restaurant_cart)
        food_list = []
        for item in cart_items:
            food_list.append(f"food : {item.food.name} - quantity : {item.quantity} - price : {item.food.price * item.quantity}")
        return food_list



class UpdateOrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['delivery_address_name','latitude','longitude']




class CreatePaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source='order.id')

    class Meta:
        model = Payment
        fields = ['order_id','origin_card_number','cvv2']


class VerifyPaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source='order.id')
    class Meta:
        model = Payment
        fields = ['order_id','origin_card_number','cvv2','daynamic_password','verification']




class ChanceSpiningPostSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source='order.id')
    class Meta:
        model = ChanceSpining
        fields = ['order_id']



class ChanceSpiningShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChanceSpining
        fields = '__all__'








