from django.shortcuts import render,get_object_or_404
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
# Create your views here.
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .serializers import *
from .models import *
from rest_framework.response import Response
from core.models import *
from account.models import *
from customer.models import *

class AdminApprovalFoodCategoryViewset(ModelViewSet):
    http_method_names = ['get','put','delete']
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        return FoodCategoryRequest.objects.all().filter(admin_approval=False).order_by('created_at')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FoodCategoryrequestShowAllSerializer
        else:
            return AdminApprovalFoodCategoryserializer


class AdminApprovalDeleteRestaurantViewset(ModelViewSet):
    http_method_names = ['get','put','delete']
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        return DeleteRestaurantRequest.objects.all().filter(admin_approval=False).order_by('created_at')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DeleteRequestShowAllSerializer
        else:
            return AdminApprovalDeleteRestaurantSerializer
