from django.urls import path , include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'owner',OwnerRegisterViews, basename='owner')




urlpatterns=[
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',UserRegisterView.as_view()),
    path('verify/',Verify.as_view()),
    path('login/',UserLoginView.as_view()),
    # path('register_owner/',OwnerRegisterView.as_view()),
    path('',include(router.urls))
]