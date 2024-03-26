from rest_framework.permissions import BasePermission
from .models import *
from account.models import *
from core.models import *

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_customer