from celery import shared_task
from django.db.transaction import atomic

from orders.business_logic.constants import OrderStatus
from transactions.constants import TransactionStatus
from transactions.models import Transaction
import logging

logger = logging.getLogger(__name__)

@shared_task
def transaction_processing_simulation():
    for transaction in Transaction.objects.filter(status=TransactionStatus.PENDING):
        with atomic():
            if transaction.order.is_paid():
                continue
            transaction.status = TransactionStatus.COMPLETED
            transaction.save()
        logger.info(f"Transaction {transaction.id} status changed to {transaction.status}")
