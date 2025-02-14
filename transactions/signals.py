from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

from orders.business_logic.constants import OrderStatus
from transactions.constants import TransactionStatus
from transactions.models import Transaction

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Transaction)
def change_order_status_on_succeeded_payment(sender, instance, created, **kwargs):
    if instance.status == TransactionStatus.COMPLETED:
        instance.order.status = OrderStatus.PROCESSING
        instance.order.save()
        logger.info(f"Order {instance.order.id} status changed to {instance.order.status}")
