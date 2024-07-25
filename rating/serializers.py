from account.models import User
from core.models import Food
from .models import Rating,RestaurantRating
from rest_framework import serializers

class RatingPostSerializer(serializers.ModelSerializer):

    food_id=serializers.IntegerField(source='food.id')

    class Meta:
        model = Rating
        fields = ('food_id','stars')

class RestaurantRatingPostSerializer(serializers.ModelSerializer):

    restaurant_id=serializers.IntegerField(source='restaurant.id')

    class Meta:
        model = RestaurantRating
        fields = ('restaurant_id','stars')


class RatingShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields ='__all__'


class RestaurantRatingShowSerializer(serializers.ModelSerializer):
    class Meta:
        model=RestaurantRating
        fields='__all__'




















