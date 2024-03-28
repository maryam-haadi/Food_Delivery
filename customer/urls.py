from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers



router = DefaultRouter()
router.register(r'address',CustomerAddress,basename='address')
router.register(r'res_list',RestaurantsListView,basename='res')
router.register(r'cofes',CofeTypeViewset,basename='cofe')
router.register(r'restarants',RestaurantTypeViewset,basename='restaurants')
router.register(r'restaurants-category',RestaurantsCategoryViewset,basename='restaurants-category')



foods_res_router=routers.NestedDefaultRouter(router,'res_list',lookup='res')
foods_res_router.register(r'foods',RestaurantFoodsViewset,basename='foods-restaurant')


restaurants_router=routers.NestedDefaultRouter(router,'res_list',lookup='res')
restaurants_router.register(r'favorite',FavoriteView,basename='restaurant-favorit')


rangeaddress_router=routers.NestedDefaultRouter(router,'address',lookup='address')
rangeaddress_router.register(r'range_address',RestaurantRangeView,basename='range-address')




urlpatterns=[
    path('',include(router.urls)),
    path('',include(restaurants_router.urls)),
    path('',include(rangeaddress_router.urls)),
    path('',include(foods_res_router.urls)),
]

