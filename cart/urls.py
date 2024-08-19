from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from django.urls import reverse


router = DefaultRouter()
# router.register(r'add_cart_items',CartItemViewset,basename='cart_item')
router.register(r'carts',CartViewset,basename='carts')
router.register(r'payment',CreatePaymentViewSet,basename='payment')
router.register(r'verifypayment',VerifyPaymentViewSet,basename='verify-payment')
router.register(r'myorders',MyOrdersViewset,basename='myorders')
router.register(r'chance_spining',ChanceSpiningViewset,basename='chance')
router.register(r'my_transactions',MyTransactions,basename='transactions')
router.register(r'chance_Dice',DiceChance,basename='chance-dice')

cart_cartitem_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_cartitem_router.register(r'items',CartItemNestedViewset,basename='cart-item')


cart_order_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_order_router.register(r'order',OrderViewset,basename='cart-order')






urlpatterns=[

    path('',include(router.urls)),
    path('',include(cart_cartitem_router.urls)),
    path('',include(cart_order_router.urls)),

]

