from decimal import Decimal
from typing import Type

from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

from common.constants import TAX_RATE
from orders.constants import OrderStatus
from prices.models import ProductPriceRecord
from transactions.constants import TransactionStatus
from transactions.models import Transaction

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Transaction)
def change_order_status_on_succeeded_payment(
    sender: Type[Transaction],
    instance: Transaction,
    created: bool,
    **kwargs
) -> None:
    if instance.status != TransactionStatus.COMPLETED.value:
        return
    instance.order.status = OrderStatus.PROCESSING.value
    instance.order.save()
    logger.info(f"Order {instance.order.id} status changed to {instance.order.status}")
    amount = Decimal(0)
    for cart_item in instance.order.cart_items.all():
        price_in_usd = cart_item.product.price * cart_item.quantity
        price_in_currency = instance.currency.rate * price_in_usd
        amount += price_in_currency
        cost_in_usd = cart_item.product.cost * cart_item.quantity
        cost_in_currency = instance.currency.rate * cost_in_usd
        ProductPriceRecord.objects.create(
            product=cart_item.product,
            price=price_in_currency,
            cost=cost_in_currency,
            quantity=cart_item.quantity,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
            currency=instance.currency,
            transaction=instance,
        )
        logger.info(f"Product {cart_item.product.id} price record created")
    tax = amount * TAX_RATE
    Transaction.objects.filter(pk=instance.pk).update(
        amount=amount,
        tax=tax,
    )
    logger.info(f"Transaction {instance.id} amount updated")
    # for correct serializer output
    instance.amount = amount
    instance.tax = tax
