import logging
import random

from celery import shared_task
from django.db import OperationalError
from django.db.transaction import atomic

from transactions.constants import TransactionStatus
from transactions.models import Transaction

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
@atomic  # atomic is used to ensure that all operations are committed or rolled back as a whole
def transaction_processing_simulation(self) -> None:
    """
    Simulate a real transaction processing by third-party service.

    bulk_update is not used here because it does not trigger pre_save and post_save signals.
    Alternatively, signals can be removed, and bulk_update can be used for better performance.
    """
    try:
        transactions = (
            Transaction.objects.select_for_update()  # lock rows for update
            .select_related("order")  # prefetch related order
            .filter(status=TransactionStatus.PENDING.value)
        )

        for transaction in transactions:
            transaction.status = random.choice(
                (
                    TransactionStatus.COMPLETED.value,
                    TransactionStatus.FAILED.value,
                )
            )
            transaction.save()
            logger.info(
                f"Transaction {transaction.id} status changed to {transaction.status}"
            )
    except OperationalError as exc:
        logger.error(f"Failed to process transactions: {exc}")
        raise self.retry(exc=exc)
