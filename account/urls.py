from django.urls import path , include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'owner',OwnerRegisterViews, basename='owner')
router.register(r'verify',VerifyView, basename='verify')
router.register(r'customer',UserRegisterView, basename='customer')
router.register(r'login',LoginView, basename='login')

urlpatterns=[
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('',include(router.urls))
]