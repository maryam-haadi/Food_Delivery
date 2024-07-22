from rest_framework import serializers
from django.shortcuts import render,get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from customer.serializers import *

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['name','last_name','phone_number']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        customer = Customer.objects.create(user=user)
        return user

class CustomerProfileUpdateSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='user.name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(
        source='user.email'
    )
    class Meta:
        model = Customer
        fields = ['name','last_name','email']

    def update(self, instance, validated_data):
        instance.user.name = validated_data['user']['name']
        instance.user.last_name = validated_data['user']['last_name']
        instance.user.email = validated_data['user']['email']
        instance.user.save()
        return instance

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model =User
        fields = ['id','name','last_name','phone_number','email']

class CustomerProfileSerializer(serializers.ModelSerializer):
    user= UserSerializer()
    class Meta:
        model=Customer
        fields=['id','user','address_name','latitude','longitude']

class CustomerAddressShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','address_name','latitude','longitude']

class CustomerAddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['address_name','latitude','longitude']





class UserVerifySerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=20)
    class Meta:
        model=User
        fields=['otp','phone_number']

class UserLoginSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=20)
    class Meta:
        model=User
        fields = ['phone_number']

class StoreTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreType
        fields = '__all__'
class OwnerRegisterSerializer(serializers.Serializer):

    choice_list =[
        ('cofe','C'),
        ('restaurant','R')
    ]

    phone_number = serializers.CharField(source='user.phone_number',max_length=20)
    name = serializers.CharField(source='user.name',max_length=255)
    last_name = serializers.CharField(source='user.last_name',max_length=255)
    email = serializers.EmailField(source='user.email',max_length=255)
    owner_address = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=200)
    stores_name = serializers.CharField(max_length=200)
    storetype_name = serializers.ChoiceField(source='type.storetype_name',choices=choice_list)
    storetype_desc = serializers.CharField(source='type.storetype_desc',max_length=255)

    def create(self, validated_data):

        user = User.objects.create_user(name=validated_data['user']['name'],
                                        last_name=validated_data['user']['last_name'],
                                        phone_number=validated_data['user']['phone_number'],
                                        email=validated_data['user']['email'])
        user.is_owner = True
        user.save()

        stype = StoreType.objects.create(storetype_name=validated_data['type']['storetype_name'],storetype_desc=validated_data['type']['storetype_desc'])
        owner = Owner.objects.create(user=user,owner_address=validated_data['owner_address'],
                                     city=validated_data['city'],stores_name=validated_data['stores_name'],
                                     type=stype)
        return owner


class OwnerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    type = StoreTypeSerializer(read_only=True)
    class Meta:
        model = Owner
        fields = ['id', 'user', 'city', 'owner_address', 'type']


class OwnerUpdateSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='user.name',max_length=255)
    last_name = serializers.CharField(source='user.last_name',max_length=255)
    email = serializers.EmailField(source='user.email',max_length=255)

    class Meta:
        model = Owner
        fields = ['name','last_name','email','owner_address','city']

    def update(self, instance, validated_data):
        user = instance.user
        user.name = validated_data['user']['name']
        user.last_name = validated_data['user']['last_name']
        user.email = validated_data['user']['email']
        user.save()
        instance.city = validated_data['city']
        instance.owner_address =validated_data['owner_address']
        instance.save()
        return instance















