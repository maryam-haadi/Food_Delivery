from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from .models import User,Customer,Address,Owner,StoreType



admin.site.register(User)
admin.site.register(Address)
admin.site.register(Customer)
admin.site.register(Owner)
admin.site.register(StoreType)