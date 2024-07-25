from django.contrib import admin
from .models import User,Customer,Owner,StoreType



admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Owner)
admin.site.register(StoreType)