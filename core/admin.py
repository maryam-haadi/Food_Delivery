from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(FoodCategory)
admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Food)
admin.site.register(Favorite)
admin.site.register(FoodCategoryRequest)
