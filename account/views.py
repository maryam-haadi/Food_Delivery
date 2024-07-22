from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework import mixins
from .serializers import *
from .models import *
import random
import requests
from customer.permissions import *
from core.permissions import *

url = "https://rest.payamak-panel.com/api/SendSMS/SendSMS"
# Create your views here.
def generate_otp(n=6):
    return "".join(map(str, random.sample(range(0, 10), n)))

class UserRegisterView(GenericViewSet,mixins.CreateModelMixin):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer


    def create(self, request, *args, **kwargs):

        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            otp_code = generate_otp(6)
            user.otp = otp_code
            user.otp_expire_time = timezone.now() + timedelta(minutes=8)
            user.is_customer = True
            user.save()
            message = f'your verification code is :{otp_code}'
            payload = {
                'username': '989116968310',
                'password': 'E8Y!4',
                'to':serializer.data['phone_number'],
                'text':message
            }
            response = requests.post(url, data=payload)
            print(response.json())
            print(otp_code)

            if response.status_code == 200:
                return Response({'message': 'message send successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'message': 'message unsend'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





class CustomerProfileViewset(ModelViewSet):
    http_method_names = ['get','put']
    permission_classes = [IsCustomer]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Customer.objects.all().filter(user=user)
        return None

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CustomerProfileUpdateSerializer
        else:
            return CustomerProfileSerializer



class CustomerAddressViewset(ModelViewSet):
    http_method_names = ['get','put']
    permission_classes = [IsCustomer]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Customer.objects.all().filter(user=self.request.user)
        return None

    def get_serializer_class(self):
        if self.request.method =='GET':
            return CustomerAddressShowSerializer
        else:
            return CustomerAddressUpdateSerializer







class VerifyView(mixins.CreateModelMixin,GenericViewSet):
    http_method_names = ['post']
    serializer_class = UserVerifySerializer
    queryset = User.objects.all().filter(is_verified=True)
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):

        serializer = UserVerifySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            otp = serializer.data['otp']
            phone_number = serializer.data['phone_number']
            user=authenticate(request,phone_number=phone_number)
            if user is not None:
                if user.otp == otp and user.otp_expire_time is not None and user.otp_expire_time > timezone.now():

                    refresh=RefreshToken.for_user(user)
                    user.otp=''
                    user.otp_expire_time=None
                    user.save()

                    user.last_login=timezone.now()
                    user.is_verified = True
                    user.save()
                    user.change_address_time = user.last_login + timedelta(hours=1)
                    return Response({'refresh': str(refresh),'access': str(refresh.access_token),},
                    status=status.HTTP_200_OK)
                else:
                    if user.otp != otp:
                        return Response({'error':'your verification code is incorrect'},status=status.HTTP_400_BAD_REQUEST)
                    if user.otp_expire_time is None or user.otp_expire_time < timezone.now():
                        return Response({'error': 'your verification code is expired time'},status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'detail':'invalid verification code or credentials'},status=status.HTTP_401_UNAUTHORIZED)









class LoginView(GenericViewSet,mixins.CreateModelMixin):
    http_method_names = ['post']
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.data['phone_number']
            user = authenticate(request, phone_number=phone_number)
            if user is not None:
                otp_code = generate_otp(6)
                print(otp_code)
                user.otp = otp_code
                user.otp_expire_time = timezone.now() + timedelta(minutes=3)
                user.is_verified = True
                user.save()

                message = f'your verification code is :{otp_code}'
                payload = {
                    'username': '989116968310',
                    'password': 'E8Y!4',
                    'to': serializer.data['phone_number'],
                    'text': message
                }
                response = requests.post(url, data=payload)
                print(response.json())

                if response.status_code == 200:
                    return Response({'message': 'verification code sent successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'message unsend'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({"error": "invalid credentials"}, status=status.HTTP_404_NOT_FOUND)








class OwnerRegisterViews(GenericViewSet,mixins.CreateModelMixin):
    http_method_names = ['post']
    queryset = Owner.objects.all()
    serializer_class = OwnerRegisterSerializer
    permission_classes = [AllowAny]


    def create(self, request, *args, **kwargs):
        serializer = OwnerRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            owner = serializer.save()
            otp_code = generate_otp(6)
            owner.user.otp = otp_code
            owner.user.otp_expire_time = timezone.now() + timedelta(minutes=8)
            owner.user.save()
            message = f'your verification code is :{otp_code}'
            payload = {
                'username': '989116968310',
                'password': 'E8Y!4',
                'to':serializer.data['phone_number'],
                'text':message
            }
            response = requests.post(url, data=payload)
            print(otp_code)
            print(response.json())

            if response.status_code == 200:
                return Response({'message': 'message send successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'message': 'message unsend'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





class OwnerProfileViewset(ModelViewSet):
    http_method_names = ['get','put']
    permission_classes = [IsOwnerRestuarant]

    def get_queryset(self):
         return Owner.objects.all().filter(user_id=self.request.user.id)


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OwnerProfileSerializer
        else:
            return  OwnerUpdateSerializer







