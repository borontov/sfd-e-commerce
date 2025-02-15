import random

from celery import shared_task
from django.db.transaction import atomic

from transactions.constants import TransactionStatus
from transactions.models import Transaction
import logging

logger = logging.getLogger(__name__)

@shared_task
def transaction_processing_simulation():
    """
    Simulate a real transaction processing by third-party service.

    bulk_update is not used here because it does not trigger pre_save and post_save signals.
    Alternatively, signals can be removed, and bulk_update can be used for better performance.
    """
    with atomic():  # atomic is used to ensure that all transactions are committed or rolled back as a whole
        transactions = (
            Transaction.objects
            .select_for_update()  # lock rows for update
            .select_related('order')  # prefetch related order
            .filter(status=TransactionStatus.PENDING)
        )

        for transaction in transactions:
            transaction.status = random.choice(
                (TransactionStatus.COMPLETED, TransactionStatus.FAILED)
            )
            transaction.save()
            logger.info(f"Transaction {transaction.id} status changed to {transaction.status}")
