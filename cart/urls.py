from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from django.urls import reverse


router = DefaultRouter()
router.register(r'add_cart_items',CartItemViewset,basename='cart_item')
router.register(r'carts',CartViewset,basename='carts')





cart_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register(r'items',CartItemNestedViewset,basename='cart-item')


#
#
# restaurants_router=routers.NestedDefaultRouter(router,'restaurants',lookup='res')
# restaurants_router.register(r'favorite',FavoriteView,basename='restaurant-favorit')





urlpatterns=[

    path('',include(router.urls)),
    path('',include(cart_router.urls))

]

