from celery import shared_task
from django.db import transaction


@shared_task
def payment_retry(order_id):
    with transaction.atomic():
        ...
