from django.shortcuts import render,get_object_or_404
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from .permissions import IsOwnerRestuarant,IsOwnerRestuarantCreate,IsMenuCreateRestaurant
# Create your views here.
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .serializers import *
from .models import *
from rest_framework.response import Response
from  customer.permissions import IsCustomer

class RestaurantView(ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        return Restaurant.objects.all().filter(owner=user.owner)


    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsOwnerRestuarantCreate()]
        elif self.request.method == 'DELETE':
            return [IsAdminUser()]
        elif self.request.method == 'GET':
            return [IsOwnerRestuarant()]
        else:
            return [IsOwnerRestuarant()]


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RestaurantShowSerializer
        else:
            return RestaurantPostSerializer


    def create(self, request, *args, **kwargs):
        serializer = RestaurantPostSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = self.request.user
            owner = user.owner
            restaurant = Restaurant.objects.create(owner=owner,**serializer.validated_data)
            return Response({"message":"create restaurant seccessfully ","data":serializer.data}
                            ,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





class MenuViewset(ModelViewSet):
    def get_queryset(self):
        user=self.request.user
        return Menu.objects.filter(restaurant__owner__user=user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsMenuCreateRestaurant()]
        else:
            return [IsOwnerRestuarant()]
    def get_serializer_class(self):
        if self.request.method =='GET':
            return MenuShowSerializer
        else:
            return MenuCreateSerializer
    def create(self, request, *args, **kwargs):
        user = request.user
        restaurant = get_object_or_404(Restaurant, owner=user.owner)
        serializer = MenuCreateSerializer(data = request.data)
        if Menu.objects.all().filter(restaurant=restaurant).first() == None:
            if serializer.is_valid(raise_exception=True):
                menu =Menu.objects.create(restaurant=restaurant,description=serializer.data['description'])
                ser = MenuShowSerializer(instance=menu)
                return Response({"message":"create menu seccessfully ","data":ser.data},status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"you can not this operation because exist menu for this restaurant "},
                            status=status.HTTP_400_BAD_REQUEST)




class FoodViewset(ModelViewSet):
    permission_classes = [IsOwnerRestuarant]
    serializer_class = FoodSerializer

    def get_queryset(self):
        menu_id = self.kwargs['menu_pk']
        return Food.objects.all().filter(menu_id=menu_id).filter(restaurant__owner__user=self.request.user)


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FoodShowSerializer
        else:
            return FoodSerializer



    def create(self, request, *args, **kwargs):
        menu_id = kwargs['menu_pk']
        restaurant = get_object_or_404(Restaurant,owner__user=request.user)
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            category=FoodCategory(category_name=serializer.validated_data['food_category']['category_name'],category_desc=serializer.validated_data['food_category']['category_desc'])
            category.save()
            food = Food.objects.create(menu_id=menu_id,restaurant=restaurant,
                                       food_category=category,
                                       image=serializer.validated_data['image'],
                                       name=serializer.validated_data['name'],desc=serializer.validated_data['desc'],
                                       price=serializer.validated_data['price'])

            return Response({"message":"add food seccessfully","data":serializer.data},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)









