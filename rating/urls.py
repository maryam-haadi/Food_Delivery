from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


router = DefaultRouter()
router.register(r'food_rating',RatingViewSetCustomerSide, basename='rating_post_customerside')
router.register(r'restaurant_rating',RestaurantRatingViewSetCustomerSide, basename='restaurant_rating_post_customerside')



urlpatterns=[
    path('',include(router.urls)),
    path('food_rates/<int:pk>',ShowFoodRatings),
    path('restaurant_rates/<int:pk>', ShowRestaurantRatings),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)