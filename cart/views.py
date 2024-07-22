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
                    item = Restaurant_cart_item.objects.all().filter(restaurant_cart=restaurant_cart).filter(food=food).first()
                    item.quantity += 1
                    item.save()

                    return Response({"message": "quantity of food plus one"},status=status.HTTP_200_OK)
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
                    order = Order.objects.all().filter(restaurant_cart=cart).filter(restaurant_cart__customer__user=request.user).first()
                    if order is not None:
                        order.delete()
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

    def __delete__(self, instance):
        instance.delete()
        order = Order.objects.all().filter(restaurant_cart=instance)\
            .filter(restaurant_cart__customer__user=self.request.user).first()
        if order is not None:
            order.delete()
        return Response({"message":"delete cart secsessfully"},status=status.HTTP_204_NO_CONTENT)





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
                    item = Restaurant_cart_item.objects.all().filter(restaurant_cart=restaurant_cart).filter(food=food).first()
                    item.quantity += 1
                    item.save()

                    return Response({"message": "quantity of food plus one"},status=status.HTTP_200_OK)
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
                    order = Order.objects.all().filter(restaurant_cart=cart).filter(restaurant_cart__customer__user=request.user).first()
                    if order is not None:
                        order.delete()

                return Response({"message":"remove this cart item from your cart"},status=status.HTTP_200_OK)
            else:
                instance.quantity = quantity
                instance.save()
                return Response({"message": "update quantity of your cartitem"}, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)






class OrderViewset(ModelViewSet):
    http_method_names = ['get','post']
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Order.objects.filter(restaurant_cart=self.kwargs['cart_pk'])\
            .filter(restaurant_cart__customer__user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddOrderSerializer
        else:
            return ShowOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = AddOrderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            restaurant_cart_id = self.kwargs['cart_pk']
            restaurant_cart = get_object_or_404(Restaurant_cart,id=restaurant_cart_id)
            cart_items = Restaurant_cart_item.objects.all().filter(restaurant_cart=restaurant_cart)\
                        .filter(restaurant_cart__customer__user=request.user)
            sum =0
            for item in cart_items:
                result = item.food.price * item.quantity
                sum += result
            sum += restaurant_cart.restaurant.delivery_price
            total_price = sum
            if Order.objects.all().filter(restaurant_cart=restaurant_cart)\
                .filter(restaurant_cart__customer__user=request.user).first() is None:
                order = Order.objects.create(restaurant_cart=restaurant_cart,total_price=total_price)
                return Response({"message":"order is created"},status=status.HTTP_201_CREATED)
            else:
                order = Order.objects.all().filter(restaurant_cart=restaurant_cart)\
                .filter(restaurant_cart__customer__user=request.user).first()
                order.delete()
                order = Order.objects.create(restaurant_cart=restaurant_cart, total_price=total_price)
                return Response({"message": "order is created"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





































