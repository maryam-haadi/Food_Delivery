from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from .models import User,Customer,Address


# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib import admin
#
# class CustomAuthenticationForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
#         self.fields.pop('password')
#
# admin.site.login_form = CustomAuthenticationForm

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Customer)
