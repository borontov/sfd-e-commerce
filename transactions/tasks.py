from celery import shared_task
from django.db.transaction import atomic

from orders.business_logic.constants import OrderStatus
from transactions.constants import TransactionStatus
from transactions.models import Transaction


@shared_task
def transaction_processing_simulation():
    for transaction in Transaction.objects.filter(status=TransactionStatus.PENDING):
        with atomic():
            transaction.status = TransactionStatus.COMPLETED
            transaction.save()
