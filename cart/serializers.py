from rest_framework import serializers
from .models import Restaurant_cart,Restaurant_cart_item
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

















