from django.shortcuts import render
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
from customer.permissions import *
from rest_framework.decorators import api_view,permission_classes
from core.permissions import *
from rating.models import *
from cart.models import *
# Create your views here.

class CommentPostViewSet(ModelViewSet):
    http_method_names = ['post']
    permission_classes = [IsCustomer]
    queryset = Comment.objects.all()
    serializer_class = CommentPostSerializer

    def create(self, request, *args, **kwargs):
        serializer=CommentPostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=request.user
            text = serializer.validated_data['text']
            id = serializer.data['food_id']
            if Rating.objects.all().filter(user=user).exists() and\
                    Order.objects.all().filter(restaurant_cart__cart_items__food__id=id).\
                filter(is_compelete=True).filter(restaurant_cart__customer__user=request.user)\
                    .first() is not None:
                food=get_object_or_404(Food,id=id)
                comment=Comment.objects.create(user=user,text=text,food=food)
                return Response({"message":"comment created seccsesfully","data":serializer.data}
                                ,status=status.HTTP_201_CREATED)

            else:
                return Response({"Error":"please at first you must rating this food or you dont have any order of this food!!"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['get'])
@permission_classes([IsAuthenticated])
def ShowFoodComments(request,pk):
    if request.method=='GET':
        food=get_object_or_404(Food,pk=pk)
        comments=Comment.objects.all().filter(food=food).filter(user__is_customer=True)
        serializer=CommentShowSerializer(instance=comments,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)


class ReplyCommentViewSet(ModelViewSet):
    http_method_names = ['get','put','delete']
    permission_classes=[IsRestuarantExist]
    def get_queryset(self):
        user=self.request.user
        restaurant=user.owner.restaurant
        return Comment.objects.all().filter(food__menu__restaurant=restaurant).filter(user__is_customer=True)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentShowSerializer
        elif self.request.method =='PUT':
            return ReplyCommentSerializer
        else:
            return CommentShowSerializer


    def update(self, request,pk):
        comment=get_object_or_404(Comment,pk=pk)
        serializer=ReplyCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            text = serializer.validated_data['text']
            reply=Comment.objects.create(user=request.user,food=comment.food,text=text)
            comment.reply=reply
            comment.save()
            return Response({"message":"data updated seccessfully","data":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)






class CommentRestaurantPostViewSet(ModelViewSet):
    http_method_names = ['post']
    permission_classes = [IsCustomer]
    queryset = Comment.objects.all()
    serializer_class = CommentRestaurantPostSerializer

    def create(self, request, *args, **kwargs):
        serializer=CommentRestaurantPostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=request.user
            if RestaurantRating.objects.all().filter(user=user).exists():
                text=serializer.validated_data['text']
                id=serializer.data['restaurant_id']
                restaurant=get_object_or_404(Restaurant,id=id)
                if Order.objects.all().filter(restaurant_cart__restaurant__id=id).\
                filter(is_compelete=True).filter(restaurant_cart__customer__user=request.user)\
                    .first() is not None:
                    comment=CommentRestaurant.objects.create(user=user,text=text,restaurant=restaurant)
                    return Response({"message":"comment created seccsesfully","data":serializer.data}
                                ,status=status.HTTP_201_CREATED)
                else:
                    return Response({"Error": "You have not ordered from this restaurant so far, so you cannot leave a comment for this restaurant."},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Error":"please at first you must rating this restaurant"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





@api_view(['get'])
@permission_classes([IsAuthenticated])
def ShowRestaurantComments(request,pk):
    if request.method=='GET':
        restaurant=get_object_or_404(Restaurant,pk=pk)
        comments=CommentRestaurant.objects.all().filter(restaurant=restaurant).filter(user__is_customer=True)
        serializer=ShowCommentRestaurantSerializer(instance=comments,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)


class ReplyCommentRestaurantViewSet(ModelViewSet):
    http_method_names = ['get','put','delete']
    permission_classes=[IsRestuarantExist]
    def get_queryset(self):
        user=self.request.user
        restaurant=user.owner.restaurant
        return CommentRestaurant.objects.all().filter(restaurant=restaurant).filter(user__is_customer=True)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShowCommentRestaurantSerializer
        elif self.request.method =='PUT':
            return ReplyCommentRestaurantSerializer
        else:
            return ShowCommentRestaurantSerializer



    def update(self, request,pk):
        comment=get_object_or_404(CommentRestaurant,pk=pk)
        serializer=ReplyCommentRestaurantSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            reply=CommentRestaurant.objects.create(user=request.user,restaurant=comment.restaurant,text=serializer.validated_data['text'])
            comment.reply=reply
            comment.save()
            return Response({"message":"data updated seccessfully","data":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



















