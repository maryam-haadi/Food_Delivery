from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from django.urls import reverse


router = DefaultRouter()
router.register(r'comment_food',CommentPostViewSet,basename='comment')
router.register(r'reply_comment_foods',ReplyCommentViewSet,basename='reply-food')
router.register(r'comment_restaurant',CommentRestaurantPostViewSet,basename='comment-restaurant')
router.register(r'reply_comment_restaurant',ReplyCommentRestaurantViewSet,basename='reply-restaurant')

urlpatterns=[
    path('',include(router.urls)),
    path('show_food_comments/<int:pk>',ShowFoodComments),
    path('show_restaurant_comments/<int:pk>',ShowRestaurantComments),
]

