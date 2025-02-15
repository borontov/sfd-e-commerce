from celery import shared_task
from django.db import OperationalError
from django.db.transaction import atomic

from orders.constants import OrderStatus
from orders.models import Order
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def cancel_order_task(self, *, order_id: int) -> None:
    try:
        with atomic():
            order = Order.objects.get(pk=order_id)
            order.status = OrderStatus.CANCELLED
            order.save()
            ... # additional refund logic

    except OperationalError as exc:
        logger.error(f"Failed to cancel order {order_id}: {exc}")
        raise self.retry(exc=exc)
