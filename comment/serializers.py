from rest_framework import serializers
from .models import *
from account.models import *
from core.models import *

class CommentPostSerializer(serializers.ModelSerializer):

    food_id = serializers.IntegerField(source='food.id')
    class Meta:
        model = Comment
        fields = ('text','food_id')




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['name','last_name','phone_number']


class FoodShowSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(source='food_category.category_name',max_length=200)
    average_rating = serializers.SerializerMethodField(method_name='get_average_rating',read_only=True)
    class Meta:
        model = Food
        fields=['id','image','category_name','name','desc','price','average_rating']

    def get_average_rating(self,obj:Food):
        ratings = obj.ratings.all()
        if not ratings:
            return 0
        rate = round(sum(rating.stars for rating in ratings)/len(ratings),2)
        obj.average_rating = rate
        return rate

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and instance.image:
            representation['image'] = request.build_absolute_uri(instance.image.url)
        return representation




class CommentShowSerializer(serializers.ModelSerializer):

    reply=serializers.SerializerMethodField(method_name='get_reply')
    user=UserSerializer()
    food=FoodShowSerializer()
    class Meta:
        model=Comment
        fields=('id','user','food','created_at','text','reply')

    def get_reply(self,obj:Comment):
        if obj.reply is not None:
            return obj.reply.text
        else:
            return None

class ReplyCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model=Comment
        fields=('text',)





class CommentRestaurantPostSerializer(serializers.ModelSerializer):

    restaurant_id = serializers.IntegerField(source='food.id')
    class Meta:
        model = CommentRestaurant
        fields = ('text','restaurant_id')



class RestaurantListSerializer(serializers.ModelSerializer):

    is_open = serializers.SerializerMethodField(method_name='get_is_active',read_only=True)
    average_rating = serializers.SerializerMethodField(method_name='get_average_rating',read_only=True)
    class Meta:
        model = Restaurant
        fields=['id','image','category','delivery_time','min_cart_price','delivery_price'
            ,'name','phone_number','open_time','close_time','address_name','latitude','longitude','is_open','average_rating']

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

    def get_average_rating(self,obj:Restaurant):
        ratings = obj.ratings.all()
        if not ratings:
            return 0
        rate = round(sum(rating.stars for rating in ratings)/len(ratings),2)
        obj.average_rating = rate
        return rate






class ShowCommentRestaurantSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    restaurant = RestaurantListSerializer()
    reply = serializers.SerializerMethodField(method_name='get_reply')
    class Meta:
        model=CommentRestaurant
        fields=('id','user','restaurant','created_at','text','reply')


    def get_reply(self,obj:CommentRestaurant):
        if obj.reply is not None:
            return obj.reply.text
        else:
            return None




class ReplyCommentRestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model=CommentRestaurant
        fields=('text',)
























































