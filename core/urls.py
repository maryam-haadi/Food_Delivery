from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register(r'res',RestaurantView, basename='restaurant')
router.register(r'menu',MenuViewset,basename='menu')




menu_router=routers.NestedDefaultRouter(router,'menu',lookup='menu')
menu_router.register(r'food',FoodViewset,basename='menu-food')




urlpatterns=[
    path('',include(router.urls)),
    path('',include(menu_router.urls)),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)