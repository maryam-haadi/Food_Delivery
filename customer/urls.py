from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from django.urls import reverse


router = DefaultRouter()

router.register(r'restaurants',RestaurantRangeView,basename='restaurants')
router.register(r'cofes',CofeTypeViewset,basename='cofe')
router.register(r'restaurants-category',RestaurantsCategoryViewset,basename='restaurants-category')





foods_res_router=routers.NestedDefaultRouter(router,'restaurants',lookup='res')
foods_res_router.register(r'foods',RestaurantFoodsViewset,basename='foods-restaurant')




restaurants_router=routers.NestedDefaultRouter(router,'restaurants',lookup='res')
restaurants_router.register(r'favorite',FavoriteView,basename='restaurant-favorit')





urlpatterns=[
    path('',include(router.urls)),
    path('',include(restaurants_router.urls)),
    path('',include(foods_res_router.urls)),
]

