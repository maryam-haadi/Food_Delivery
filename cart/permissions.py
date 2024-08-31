from rest_framework.permissions import BasePermission
from .models import *
from account.models import *
from core.models import *
from .models import *


class HaveChance(BasePermission):
    def has_permission(self, request, view):
        customer = Customer.objects.all().filter(user=request.user).first()
        return request.user and request.user.is_authenticated and request.user.is_customer and Order.objects\
            .all().filter(paid=False).filter(total_price__gt=500000).exists() and customer.score >= 100


class HaveChanceDice(BasePermission):
    def has_permission(self, request, view):
        customer = Customer.objects.all().filter(user=request.user).first()
        return request.user and request.user.is_authenticated and request.user.is_customer and Order.objects\
            .all().filter(paid=False).filter(total_price__lte=500000).exists() and customer.score >= 100