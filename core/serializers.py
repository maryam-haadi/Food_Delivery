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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and instance.image:
            representation['image'] = request.build_absolute_uri(instance.image.url)
        return representation



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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and instance.image:
            representation['image'] = request.build_absolute_uri(instance.image.url)
        return representation





class RestaurantPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields=['image','category','delivery_time','min_cart_price','delivery_price'
            ,'name','phone_number','open_time','close_time','address_name','latitude','longitude']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and instance.image:
            representation['image'] = request.build_absolute_uri(instance.image.url)
        return representation




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

    class Meta:
        model = Food
        fields=['image','food_category','name','desc','price']

    def update(self, instance, validated_data):
        instance.food_category = validated_data['food_category']
        instance.image = validated_data['image']
        instance.name = validated_data['name']
        instance.desc = validated_data['desc']
        instance.price = validated_data['price']
        instance.save()
        return instance


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and instance.image:
            representation['image'] = request.build_absolute_uri(instance.image.url)
        return representation


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



class FoodCategoryRequestPostSerializer(serializers.ModelSerializer):
    class Meta:
        model=FoodCategoryRequest
        fields=['cat_name','cat_desc']

class FoodCategoryRequestShowSerializer(serializers.ModelSerializer):
    class Meta:
        model=FoodCategoryRequest
        fields=['id','cat_name','cat_desc','admin_approval']





class DeleteRestaurantRequestPostSerializer(serializers.ModelSerializer):
    class Meta:
        model=DeleteRestaurantRequest
        fields=['desc']

class DeleteRestaurantRequestShowSerializer(serializers.ModelSerializer):
    class Meta:
        model=DeleteRestaurantRequest
        fields=['id','desc','admin_approval']





