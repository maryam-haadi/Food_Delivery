from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
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
from customer.permissions import *
from rest_framework.decorators import action
from core.serializers import *
from account.serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rating.models import *
from rating.serializers import *
from .serializers import *
# Create your views here.





class CartItemViewset(ModelViewSet):
    permission_classes = [IsCustomer]
    http_method_names = ['post','get','put']

    def get_queryset(self):
        return Restaurant_cart_item.objects.all().filter(restaurant_cart__customer__user = self.request.user)
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return Addcartitemserializer
        elif self.request.method == 'GET':
            return Showcartitemserializer
        else:
            return Updatecartitemserializer


    def create(self, request, *args, **kwargs):
        serializer = Addcartitemserializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            food_id = serializer.validated_data['food']['pk']
            food = get_object_or_404(Food,id=food_id)
            restaurant = food.menu.restaurant
            user = request.user
            customer = get_object_or_404(Customer,user=user)

            restaurant_cart,created = Restaurant_cart.objects.get_or_create(customer=customer,restaurant=restaurant)
            if created:
                restaurant_cart_item = Restaurant_cart_item.objects.create(restaurant_cart=restaurant_cart,food=food)
                return Response({"message":"created succsesfully","data":serializer.data},status=status.HTTP_201_CREATED)

            else:
                if Restaurant_cart_item.objects.all().filter(restaurant_cart=restaurant_cart).filter(food=food).first() is None:
                    restaurant_cart_item = Restaurant_cart_item.objects.create(restaurant_cart=restaurant_cart,food=food)
                    return Response({"message":"created succsesfully","data":serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({"message": "this food already exist in your cart you can update quantity of food"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk):
        instance = get_object_or_404(Restaurant_cart_item,pk=pk)
        serializer = Updatecartitemserializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            quantity = serializer.validated_data['quantity']
            if quantity == 0:
                instance.delete()
                cart = instance.restaurant_cart
                if Restaurant_cart_item.objects.all().filter(restaurant_cart=cart).first() is None:
                    cart.delete()
                return Response({"message":"remove this cart item from your cart"},status=status.HTTP_200_OK)
            else:
                instance.quantity = quantity
                instance.save()
                return Response({"message": "update quantity of your cartitem"}, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class CartViewset(ModelViewSet):
    permission_classes = [IsCustomer]
    http_method_names = ['get','delete']
    serializer_class = CartShowSerializer

    def get_queryset(self):
        return Restaurant_cart.objects.all().filter(customer__user=self.request.user)





class CartItemNestedViewset(ModelViewSet):
    permission_classes = [IsCustomer]
    http_method_names = ['post','get','put']

    def get_queryset(self):
        print(self.kwargs['cart_pk'])
        return Restaurant_cart_item.objects.all().filter(restaurant_cart__customer__user = self.request.user).filter(restaurant_cart_id=self.kwargs['cart_pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return Addcartitemserializer
        elif self.request.method == 'GET':
            return Showcartitemserializer
        else:
            return Updatecartitemserializer


    def create(self, request, *args, **kwargs):
        serializer = Addcartitemserializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            food_id = serializer.validated_data['food']['pk']
            food = get_object_or_404(Food,id=food_id)
            restaurant = food.menu.restaurant
            user = request.user
            customer = get_object_or_404(Customer,user=user)

            restaurant_cart,created = Restaurant_cart.objects.get_or_create(customer=customer,restaurant=restaurant)
            if created:
                restaurant_cart_item = Restaurant_cart_item.objects.create(restaurant_cart=restaurant_cart,food=food)
                return Response({"message":"created succsesfully","data":serializer.data},status=status.HTTP_201_CREATED)

            else:
                if Restaurant_cart_item.objects.all().filter(restaurant_cart=restaurant_cart).filter(food=food).first() is None:
                    restaurant_cart_item = Restaurant_cart_item.objects.create(restaurant_cart=restaurant_cart,food=food)
                    return Response({"message":"created succsesfully","data":serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({"message": "this food already exist in your cart you can update quantity of food"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




    def update(self,request,pk,**kwargs):
        instance = get_object_or_404(Restaurant_cart_item,pk=pk)
        serializer = Updatecartitemserializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            quantity = serializer.validated_data['quantity']
            if quantity == 0:
                instance.delete()
                cart = instance.restaurant_cart
                if Restaurant_cart_item.objects.all().filter(restaurant_cart=cart).first() is None:
                    cart.delete()
                return Response({"message":"remove this cart item from your cart"},status=status.HTTP_200_OK)
            else:
                instance.quantity = quantity
                instance.save()
                return Response({"message": "update quantity of your cartitem"}, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



















