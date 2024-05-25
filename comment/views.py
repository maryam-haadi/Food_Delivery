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
            if Rating.objects.all().filter(user=user).exists():
                text=serializer.validated_data['text']
                id=serializer.data['food_id']
                food=get_object_or_404(Food,id=id)
                comment=Comment.objects.create(user=user,text=text,food=food)
                return Response({"message":"comment created seccsesfully","data":serializer.data}
                                ,status=status.HTTP_201_CREATED)

            else:
                return Response({"Error":"please at first you must rating this food"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['get'])
@permission_classes([IsAuthenticated])
def ShowFoodComments(request,pk):
    if request.method=='GET':
        food=get_object_or_404(Food,pk=pk)
        comments=food.comments
        serializer=CommentShowSerializer(instance=comments,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)


class ReplyCommentViewSet(ModelViewSet):
    http_method_names = ['get','put']
    permission_classes=[IsRestuarantExist]
    def get_queryset(self):
        user=self.request.user
        restaurant=user.owner.restaurant
        return Comment.objects.all().filter(reply=None,food__menu__restaurant=restaurant)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentShowSerializer
        elif self.request.method =='PUT':
            return ReplyCommentSerializer


    def update(self, request,pk):
        comment=get_object_or_404(Comment,pk=pk)
        serializer=ReplyCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            reply=Comment.objects.create(user=request.user,food=comment.food)
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
                comment=CommentRestaurant.objects.create(user=user,text=text,restaurant=restaurant)
                return Response({"message":"comment created seccsesfully","data":serializer.data}
                                ,status=status.HTTP_201_CREATED)

            else:
                return Response({"Error":"please at first you must rating this restaurant"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['get'])
@permission_classes([IsAuthenticated])
def ShowRestaurantComments(request,pk):
    if request.method=='GET':
        restaurant=get_object_or_404(Restaurant,pk=pk)
        comments=restaurant.comments
        serializer=CommentRestaurantShowSerializer(instance=comments,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)


class ReplyCommentRestaurantViewSet(ModelViewSet):
    http_method_names = ['get','put']
    permission_classes=[IsRestuarantExist]
    def get_queryset(self):
        user=self.request.user
        restaurant=user.owner.restaurant
        return CommentRestaurant.objects.all().filter(reply=None,restaurant=restaurant)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentRestaurantShowSerializer
        elif self.request.method =='PUT':
            return ReplyCommentRestaurantSerializer


    def update(self, request,pk):
        comment=get_object_or_404(CommentRestaurant,pk=pk)
        serializer=ReplyCommentRestaurantSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            reply=CommentRestaurant.objects.create(user=request.user,restaurant=comment.restaurant)
            comment.reply=reply
            comment.save()
            return Response({"message":"data updated seccessfully","data":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



















