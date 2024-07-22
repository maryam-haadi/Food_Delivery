from rest_framework import serializers
from .models import Restaurant_cart,Restaurant_cart_item,Order,Payment
from core.serializers import FoodShowSerializer
from core.models import Restaurant

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
    class Meta:
        model = Restaurant_cart
        fields =['id','restaurant','created_at','updated_at']


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



class AddOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model =Order
        fields = []

class ShowOrderSerializer(serializers.ModelSerializer):

    delivery_price = serializers.SerializerMethodField(method_name='get_delivery_price',read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price',read_only=True)
    total_order = serializers.SerializerMethodField(method_name='get_total_order',read_only=True)
    class Meta:
        model = Order
        fields = ['id','delivery_price','total_order','total_price']

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










