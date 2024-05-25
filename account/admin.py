from django.contrib import admin
from .models import User,Customer,Owner,StoreType,Address



admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Owner)
admin.site.register(StoreType)
admin.site.register(Address)