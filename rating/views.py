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
from rest_framework import filters
from rating.models import *
from rating.serializers import *
from rest_framework.decorators import api_view,permission_classes
from core.permissions import *
from customer.permissions import *
# Create your views here.

class RatingViewSetCustomerSide(GenericViewSet,mixins.CreateModelMixin):
    http_method_names = ['post']
    permission_classes = [IsCustomer]
    queryset = Rating.objects.all()
    serializer_class = RatingPostSerializer

    def create(self, request, *args, **kwargs):
        serializer=RatingPostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            food=get_object_or_404(Food,pk=serializer.data['food_id'])
            if Rating.objects.filter(user=request.user,food=food).exists():
                return Response({"error":"you rated this food recently"})
            else:
                 if Order.objects.all().filter(restaurant_cart__cart_items__food=food). \
                    filter(is_compelete=True).filter(restaurant_cart__customer__user=request.user) \
                    .first() is not None:
                    rating=Rating.objects.create(user=request.user,food=food,stars=serializer.data['stars'])
                    return Response({"message":"you rated successfully","data":serializer.data},status=status.HTTP_201_CREATED)
                 else:
                     return Response({"Error message":"You have not ordered this food yet, so you cannot rate it."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['get'])
@permission_classes([IsAuthenticated])
def ShowFoodRatings(request,pk):
    if request.method == 'GET':
        food=get_object_or_404(Food,pk=pk)
        rates=food.ratings
        serializer=RatingShowSerializer(instance=rates,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)

class RestaurantRatingViewSetCustomerSide(GenericViewSet,mixins.CreateModelMixin):
    http_method_names = ['post']
    permission_classes = [IsCustomer]
    queryset = RestaurantRating.objects.all()
    serializer_class = RestaurantRatingPostSerializer

    def create(self, request, *args, **kwargs):
        serializer=RestaurantRatingPostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            restaurant=get_object_or_404(Restaurant,pk=serializer.data['restaurant_id'])
            if RestaurantRating.objects.filter(user=request.user,restaurant=restaurant).exists():
                return Response({"error":"you rated this restaurant recently"})
            else:
                if Order.objects.all().filter(restaurant_cart__restaurant=restaurant). \
                        filter(is_compelete=True).filter(restaurant_cart__customer__user=request.user) \
                        .first() is not None:
                    rating=RestaurantRating.objects.create(user=request.user,restaurant=restaurant,stars=serializer.data['stars'])
                    return Response({"message":"you rated successfully","data":serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({"message":"You have never ordered from this restaurant, so you cannot rate this restaurant."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['get'])
@permission_classes([IsAuthenticated])
def ShowRestaurantRatings(request,pk):
    if request.method == 'GET':
        restaurant=get_object_or_404(Restaurant,pk=pk)
        rates=restaurant.ratings
        serializer=RestaurantRatingShowSerializer(instance=rates,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)






class ShowListOfRestaurantRatingsViewset(ModelViewSet):
    http_method_names = ['get']
    permission_classes = [IsRestuarantExist]
    serializer_class = ShowListOfRestaurantRatingsSerializer

    def get_queryset(self):
        return RestaurantRating.objects.all().filter(restaurant__owner__user=self.request.user)


class ShowListOfFoodRatingsViewset(ModelViewSet):
    http_method_names = ['get']
    permission_classes = [IsRestuarantExist]
    serializer_class = ShowListOfFoodRatingsSerializer

    def get_queryset(self):
        return Rating.objects.all().filter(food__menu__restaurant__owner__user=self.request.user)

















