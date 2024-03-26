from rest_framework import serializers
from .models import *
from account.models import *
from .models import *
from rest_framework import serializers
from datetime import  timedelta, datetime
from math import radians,sin,cos,sqrt,asin

class RestaurantShowSerializer(serializers.ModelSerializer):

    is_open = serializers.SerializerMethodField(method_name='get_is_active',read_only=True)
    class Meta:
        model = Restaurant
        fields=['id','image','category','delivery_time','min_cart_price','delivery_price'
            ,'name','phone_number','open_time','close_time','address_name','latitude','longitude','is_open']

    def get_is_active(self,restaurant:Restaurant):

        check =False
        if datetime.now().time() < restaurant.close_time and datetime.now().time() > restaurant.open_time:
            check = True
        else:
            check = False
        return check



class RestaurantListSerializer(serializers.ModelSerializer):

    is_open = serializers.SerializerMethodField(method_name='get_is_active',read_only=True)
    class Meta:
        model = Restaurant
        fields=['id','image','category','delivery_time','min_cart_price','delivery_price'
            ,'name','phone_number','open_time','close_time','address_name','latitude','longitude','is_open']

    def get_is_active(self,restaurant:Restaurant):
        if datetime.now().time() < restaurant.close_time and datetime.now().time() > restaurant.open_time:
            check = True
        else:
            check = False
        return check





class RestaurantPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields=['image','category','delivery_time','min_cart_price','delivery_price'
            ,'name','phone_number','open_time','close_time','address_name','latitude','longitude']




class FavoritPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = []


class FavoriteListSerializer(serializers.ModelSerializer):


    restaurant = RestaurantShowSerializer(read_only=True)
    class Meta:
        model = Favorite
        fields=['id','user','restaurant']



class MenuCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ['description']


class MenuShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = '__all__'


class FoodSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(source='food_category.category_name',max_length=200)
    category_desc = serializers.CharField(source='food_category.category_desc',max_length=255)
    class Meta:
        model = Food
        fields=['image','category_name','category_desc','name','desc','price']

    def update(self, instance, validated_data):
        food_category = instance.food_category
        food_category.category_name = validated_data['food_category']['category_name']
        food_category.category_desc = validated_data['food_category']['category_desc']
        food_category.save()
        instance.food_category = food_category
        instance.image = validated_data['image']
        instance.name = validated_data['name']
        instance.desc = validated_data['desc']
        instance.price = validated_data['price']
        instance.save()
        return instance


class FoodShowSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(source='food_category.category_name',max_length=200)
    category_desc = serializers.CharField(source='food_category.category_desc',max_length=255)
    class Meta:
        model = Food
        fields=['id','image','category_name','category_desc','name','desc','price']



