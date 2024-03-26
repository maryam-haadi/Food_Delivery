from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework import mixins
from .serializers import *
from .models import *
from .permissions import IsCustomer
# from django.contrib.gis.measure import D
# from django.contrib.gis.geos import Point
from rest_framework.decorators import action
# Create your views here.
from django.db.models import F, Value
class CustomerAddress(ModelViewSet):
    permission_classes = [IsCustomer]
    def get_queryset(self):
        user = self.request.user
        return Address.objects.all().filter(user=user)


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShowAddressSerializer
        else:
            return AddressSerializer


    def create(self, request, *args, **kwargs):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            address_name =serializer.data['address_name']
            latitude = serializer.data['latitude']
            longitude = serializer.data['longitude']
            address = Address.objects.create(address_name=address_name
                                             ,latitude=latitude,longitude=longitude)
            address.user.add(request.user)
            return Response({"message":"seccessfully create address","data":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


def get_distance(user_lat,user_long,res_lat,res_long):

    earth_radius = 6371

    user_lat = radians(user_lat)
    user_long = radians(user_long)
    restaurant_lat = radians(res_lat)
    restaurant_long = radians(res_long)
    dlon = restaurant_long - user_long
    dlat = restaurant_lat - user_lat
    a=sin(dlat/2)*sin(dlat/2) + cos(user_lat) * cos(restaurant_lat) * sin(dlon/2) *sin(dlon/2)
    c=2* asin(sqrt(a))
    distance = earth_radius * c
    return distance




class RestaurantRangeView(GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):

    queryset = Restaurant.objects.all()
    permission_classes = [IsCustomer]

    http_method_names = ['get']


    serializer_class = RestaurantRangeSerializer

    def get_serializer_context(self):
        return {"a_id":self.kwargs['address_pk']}

    def list(self, request, *args, **kwargs):
        nearby_restaurant =[]
        distances=[]
        address_id =self.kwargs['address_pk']
        user_addr=get_object_or_404(Address,id=address_id)
        restaurants = Restaurant.objects.all()
        for restaurant in restaurants:
            distance =get_distance(user_addr.latitude,user_addr.longitude,
                                   restaurant.latitude,restaurant.longitude)
            if distance < 5000:
                nearby_restaurant.append(restaurant)
                distances.append(distance)

        serializer = self.get_serializer(nearby_restaurant,many=True)
        return Response({"distance":distances,"data":serializer.data})
















class RestaurantListView(GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantListSerializer
    permission_classes = [IsCustomer]



class FavoriteView(ModelViewSet):
    http_method_names = ['get','post','delete']
    permission_classes = [IsCustomer]

    def get_queryset(self):
        user = self.request.user
        return Favorite.objects.all().filter(user=user)

    def get_serializer_class(self):
        if self.request.method =='GET':
            return FavoriteListSerializer
        elif self.request.method == 'POST':
            return FavoritPostSerializer
        else:
            return FavoritPostSerializer


    def create(self, request, *args, **kwargs):
        user_id =request.user.id
        restaurant_id = kwargs['res_pk']
        if Favorite.objects.all().filter(user_id=user_id).filter(restaurant_id=restaurant_id).first() == None:
            favorite =Favorite.objects.create(user_id=user_id,restaurant_id=restaurant_id)
            serializer = FavoriteListSerializer(instance=favorite)
            return Response({"message":"seccessfully saved","data":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"Error":"you can not this operation"},status=status.HTTP_400_BAD_REQUEST)





















