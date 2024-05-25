from django.urls import path , include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'owner_register',OwnerRegisterViews, basename='owner-register')
router.register(r'owner_profile',OwnerProfileViewset, basename='owner-profile')
router.register(r'verify',VerifyView, basename='verify')
router.register(r'customer_register',UserRegisterView, basename='customer_register')
router.register(r'customer_profile',CustomerProfileViewset, basename='customer-profile')
router.register(r'login',LoginView, basename='login')

urlpatterns=[
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('',include(router.urls))
]