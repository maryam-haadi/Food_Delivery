from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from django.urls import reverse


router = DefaultRouter()
router.register(r'comment',CommentPostViewSet,basename='comment')
router.register(r'reply',ReplyCommentViewSet,basename='reply')

urlpatterns=[
    path('',include(router.urls)),
    path('show_comments/<int:pk>',ShowFoodComments),
]

