from rest_framework import serializers
from .models import *
from account.models import *

class CommentPostSerializer(serializers.ModelSerializer):

    food_id = serializers.IntegerField(source='food.id')
    class Meta:
        model = Comment
        fields = ('text','food_id')


class ShowCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields='__all__'


class CommentShowSerializer(serializers.ModelSerializer):

    reply=ShowCommentSerializer()
    class Meta:
        model=Comment
        fields=('user','food','created_at','text','reply')

class ReplyCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model=Comment
        fields=('text',)





class CommentRestaurantPostSerializer(serializers.ModelSerializer):

    restaurant_id = serializers.IntegerField(source='food.id')
    class Meta:
        model = CommentRestaurant
        fields = ('text','restaurant_id')


class ShowCommentRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model=CommentRestaurant
        fields='__all__'


class CommentRestaurantShowSerializer(serializers.ModelSerializer):

    reply=ShowCommentRestaurantSerializer()
    class Meta:
        model=CommentRestaurant
        fields=('user','restaurant','created_at','text','reply')

class ReplyCommentRestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model=CommentRestaurant
        fields=('text',)
























































