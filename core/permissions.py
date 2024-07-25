from rest_framework.permissions import BasePermission
from .models import *
class IsOwnerRestuarantCreate(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        return request.user and request.user.is_authenticated\
            and request.user.is_owner and\
            Restaurant.objects.all().filter(owner=user.owner).first() == None

class IsOwnerRestuarant(BasePermission):
    def has_permission(self, request, view):

        return request.user and request.user.is_authenticated\
            and request.user.is_owner



class IsRestuarantExist(BasePermission):
    def has_permission(self, request, view):

        return request.user and request.user.is_authenticated\
            and request.user.is_owner and Restaurant.objects.all().filter(owner__user=request.user).first()!=None









# class IsMenuCreateRestaurant(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.is_authenticated and\
#             request.user.is_owner and\
#             Restaurant.objects.all().filter(owner__user=request.user).first() !=None and\
#             Menu.objects.all().filter(restaurant__owner__user=request.user).first() == None
#
# class IsMenuExistRestaurant(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.is_authenticated and\
#             request.user.is_owner and\
#             Restaurant.objects.all().filter(owner__user=request.user).first() !=None and\
#             Menu.objects.all().filter(restaurant__owner__user=request.user).first() != None


