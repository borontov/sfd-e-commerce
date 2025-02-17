import logging

from celery import shared_task
from django.db import OperationalError
from django.db.transaction import atomic

from orders.constants import OrderStatus
from orders.models import Order

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
@atomic  # atomic is used to ensure that all operations are committed or rolled back as a whole
def cancel_order_task(self, *, order_id: int) -> None:
    try:
        order = Order.objects.get(pk=order_id)
        order.status = OrderStatus.CANCELLED.value
        order.save()
        ...  # additional refund logic

    except OperationalError as exc:
        logger.error(f"Failed to cancel order {order_id}: {exc}")
        raise self.retry(exc=exc)
