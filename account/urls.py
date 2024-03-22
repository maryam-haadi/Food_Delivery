from django.urls import path , include
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns=[
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',UserRegisterView.as_view()),
    path('verify/',Verify.as_view()),
    path('login/',UserLoginView.as_view()),
]