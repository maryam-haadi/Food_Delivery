# myapp/tasks.py
from celery import shared_task
from account.models import Customer
from django.utils import timezone
from datetime import timedelta
@shared_task
def null_address():
    customers = Customer.objects.all()
    for c in customers:
        if c.address is not None:
            if c.user.change_address_time <= timezone.now():
                c.address = None
                c.save()

