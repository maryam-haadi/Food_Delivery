from rest_framework import serializers
from .models import *
from account.models import *
from core.models import *
from datetime import  timedelta, datetime
from math import radians,sin,cos,sqrt,asin
from core.serializers import *
from account.serializers import *


class ShowAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields=['id','address_name','latitude','longitude']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields=['address_name','latitude','longitude']

class RestaurantListSerializer(serializers.ModelSerializer):
    is_open = serializers.SerializerMethodField(method_name='get_is_active', read_only=True)
    class Meta:
        model = Restaurant
        fields = ['id', 'image', 'category', 'delivery_time', 'min_cart_price', 'delivery_price'
            ,'name', 'phone_number', 'open_time', 'close_time', 'address_name', 'latitude', 'longitude','is_open']

    def get_is_active(self, restaurant: Restaurant):
        if datetime.now().time() < restaurant.close_time and datetime.now().time() > restaurant.open_time:
            check = True
        else:
            check = False
        return check



class FavoritPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = []


class FavoriteListSerializer(serializers.ModelSerializer):


    restaurant = RestaurantShowSerializer(read_only=True)
    class Meta:
        model = Favorite
        fields=['id','user','restaurant']



class RestaurantRangeSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField(method_name='get_distance',read_only=True)
    is_open = serializers.SerializerMethodField(method_name='get_is_active', read_only=True)
    class Meta:
        model = Restaurant
        fields =['id','image','category','delivery_time','min_cart_price','delivery_price'
            ,'name','phone_number','open_time','close_time','address_name','latitude','longitude','is_open','distance']


    def get_distance(self,restaurant:Restaurant):
        address_id = self.context['a_id']
        user_address = Address.objects.all().filter(id=address_id).first()
        earth_radius = 6371

        user_lat = radians(user_address.latitude)
        user_long = radians(user_address.longitude)
        restaurant_lat = radians(restaurant.latitude)
        restaurant_long = radians(restaurant.longitude)
        dlon = restaurant_long - user_long
        dlat = restaurant_lat - user_lat
        a=sin(dlat/2)*sin(dlat/2) + cos(user_lat) * cos(restaurant_lat) * sin(dlon/2) *sin(dlon/2)
        c=2* asin(sqrt(a))
        distance = earth_radius * c
        return distance

    def get_is_active(self,restaurant:Restaurant):
        if datetime.now().time() < restaurant.close_time and datetime.now().time() > restaurant.open_time:
            check = True
        else:
            check = False
        return check





