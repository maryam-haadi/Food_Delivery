from rest_framework import serializers
from .models import *
from account.models import *
from core.models import *
from customer.models import *
from datetime import  timedelta, datetime
from math import radians,sin,cos,sqrt,asin
from core.serializers import *
from account.serializers import *


class ShowAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields=['id','address_name','latitude','longitude']

class CustomerShowSelectedAddressSerializer(serializers.ModelSerializer):
    address=ShowAddressSerializer()
    class Meta:
        model=Customer
        fields=('id','user','address')





class CustomerSelectAddressSerializer(serializers.ModelSerializer):
    address_id = serializers.IntegerField()

    class Meta:
        model=Customer
        fields=['address_id']


    def validate(self, attrs):
        address = get_object_or_404(Address,id=attrs['address_id'])
        if address.user != self.context['request'].user:
            raise serializers.ValidationError("this address id is not correct!")
        return attrs


    def update(self, instance, validated_data):
        address= get_object_or_404(Address,id=validated_data['address_id'])
        instance.address = address
        instance.save()
        return instance




class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields=['address_name','latitude','longitude']

class RestaurantListSerializer(serializers.ModelSerializer):
    is_open = serializers.SerializerMethodField(method_name='get_is_active', read_only=True)
    average_rating = serializers.SerializerMethodField(method_name='get_average_rating')
    class Meta:
        model = Restaurant
        fields = ['id', 'image', 'category', 'delivery_time', 'min_cart_price', 'delivery_price'
            ,'name', 'phone_number', 'open_time', 'close_time', 'address_name', 'latitude', 'longitude','is_open','average_rating']

    def get_is_active(self, restaurant: Restaurant):
        if datetime.now().time() < restaurant.close_time and datetime.now().time() > restaurant.open_time:
            check = True
        else:
            check = False
        return check

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
    average_rating = serializers.SerializerMethodField(method_name='get_average_rating')
    class Meta:
        model = Restaurant
        fields =['id','image','category','delivery_time','min_cart_price','delivery_price'
            ,'name','phone_number','open_time','close_time','address_name','latitude','longitude','is_open','distance','average_rating']


    def get_distance(self,restaurant:Restaurant):
        user=self.context['user']
        customer=get_object_or_404(Customer,user=user)
        user_address = customer.address
        if user_address is None:
            return None
        else:
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



class FoodShowForCustomersSerializer(serializers.ModelSerializer):

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


















