from django.urls import path,include
from django.conf import settings
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


router = DefaultRouter()
router.register(r'food_category_requests',AdminApprovalFoodCategoryViewset, basename='food-category-requests')
router.register(r'delete_restaurant_request',AdminApprovalDeleteRestaurantViewset, basename='delete-restaurant-request')

urlpatterns=[
    path('',include(router.urls)),
]