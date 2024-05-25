from rest_framework import serializers
from account.models import *
from core.models import *
from customer.models import *

class AdminApprovalFoodCategoryserializer(serializers.ModelSerializer):
    class Meta:
        model=FoodCategoryRequest
        fields=['admin_approval']

    def update(self, instance, validated_data):
        instance.admin_approval = validated_data['admin_approval']
        instance.save()
        if instance.admin_approval == True and FoodCategory.objects.all().filter(category_name=instance.cat_name).first()== None:
            food_category = FoodCategory.objects.create(category_name=instance.cat_name)
        return instance


class FoodCategoryrequestShowAllSerializer(serializers.ModelSerializer):
    class Meta:
        model=FoodCategoryRequest
        fields='__all__'




class AdminApprovalDeleteRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model=DeleteRestaurantRequest
        fields=['admin_approval']

    def update(self, instance, validated_data):
        instance.admin_approval = validated_data['admin_approval']
        instance.save()
        if instance.admin_approval == True and Restaurant.objects.all().filter(id=instance.restaurant.id).first()!=None:
            restaurant =  Restaurant.objects.all().filter(id=instance.restaurant.id).first()
            restaurant.delete()

        return instance


class DeleteRequestShowAllSerializer(serializers.ModelSerializer):
    class Meta:
        model=DeleteRestaurantRequest
        fields='__all__'





