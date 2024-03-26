from django.db import models
from account.models import *
from core.models import *
# Create your models here.
class Address(models.Model):
    user = models.ManyToManyField('account.User',related_name='address')
    address_name = models.CharField(max_length=200,default='')
    latitude = models.FloatField()
    longitude = models.FloatField()