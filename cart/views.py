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
    def get_distance(self,user_lat, user_long, res_lat, res_long):

        earth_radius = 6371

        user_lat = radians(user_lat)
        user_long = radians(user_long)
        restaurant_lat = radians(res_lat)
        restaurant_long = radians(res_long)
        dlon = restaurant_long - user_long
        dlat = restaurant_lat - user_lat
        a = sin(dlat / 2) * sin(dlat / 2) + cos(user_lat) * cos(restaurant_lat) * sin(dlon / 2) * sin(dlon / 2)
        c = 2 * asin(sqrt(a))
        distance = earth_radius * c
        return distance


    http_method_names = ['get','put']
    permission_classes = [IsCustomer]

    def get_serializer_context(self):
        res_cart = get_object_or_404(Restaurant_cart,pk=self.kwargs['cart_pk'])

        return {"min_price":res_cart.restaurant.min_cart_price}

    def get_queryset(self):
        if Order.objects.filter(restaurant_cart=self.kwargs['cart_pk']).filter(restaurant_cart__customer__user=self.request.user).first() is None:
            customer = Customer.objects.all().filter(user=self.request.user).first()
            order = Order.objects.create(restaurant_cart_id=self.kwargs['cart_pk'],
                                         delivery_address_name=customer.address_name,
                                         latitude=customer.latitude,
                                         longitude=customer.longitude)
            print(order.total_price)


            return Order.objects.filter(restaurant_cart=self.kwargs['cart_pk'])\
                .filter(restaurant_cart__customer__user=self.request.user)
        else:
            order = Order.objects.filter(restaurant_cart=self.kwargs['cart_pk'])\
                .filter(restaurant_cart__customer__user=self.request.user).first()

            total_price = order.total_price
            delivery_price = order.restaurant_cart.restaurant.delivery_price
            total_order = total_price - delivery_price
            # if total_order < order.restaurant_cart.restaurant.min_cart_price:
            #     return  Response({"message":"errorrr"})
            return Order.objects.filter(restaurant_cart=self.kwargs['cart_pk'])\
                .filter(restaurant_cart__customer__user=self.request.user)


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShowOrderSerializer
        else:
            return UpdateOrderAddressSerializer



    def update(self, request,pk,**kwargs):
        order = get_object_or_404(Order,pk=pk)
        serializer = UpdateOrderAddressSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            restaurant_cart_pk = self.kwargs['cart_pk']
            res_cart = get_object_or_404(Restaurant_cart,pk=restaurant_cart_pk)
            restaurant = res_cart.restaurant
            customer_lat = serializer.validated_data['latitude']
            customer_long = serializer.validated_data['longitude']

            dist = self.get_distance(customer_lat,customer_long,restaurant.latitude,restaurant.longitude)
            print("distance",dist)
            if dist > 5000:
                return Response({"message":"Your selected address is outside the restaurant area"},status=status.HTTP_400_BAD_REQUEST)
            else:
                order.delivery_address_name = serializer.validated_data['delivery_address_name']
                order.latitude = customer_lat
                order.longitude = customer_long
                order.save()
                return Response({"message":"updated address sucssesfully","data":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)






































