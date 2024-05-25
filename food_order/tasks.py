from celery import shared_task
from account.models import Customer

@shared_task
def set_field_to_null():
    Customer.objects.all().update(address=None)