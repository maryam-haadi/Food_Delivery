from rest_framework import serializers
from .models import User,Address,Customer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['name','last_name','phone_number']

    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        customer = Customer.objects.create(user=user)
        return user


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