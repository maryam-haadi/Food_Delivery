from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register(r'res',RestaurantView, basename='restaurant')
router.register(r'add_food',FoodViewset,basename='food')
router.register(r'category_request',FoodCategoryRequestViewset,basename='category-request')
router.register(r'delete_request',DeleteRestaurantRequestViewset,basename='delete-request')
router.register(r'food_category',FoodCategoryViewset,basename='food-category')
router.register(r'restaurants_orders',RestaurantsOrderViewset,basename='orders')



urlpatterns=[
    path('',include(router.urls)),

]
