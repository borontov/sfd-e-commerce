from django.db import models

from common.models import BaseModel
from orders.constants import OrderStatus
from transactions.constants import TransactionStatus


class Order(BaseModel):
    """
    Represents customer orders and their current status.
    Links to cart items and tracks payment status through related transactions.
    """

    email = models.EmailField()
    cart_items = models.ManyToManyField("orders.OrderCartItem")
    status = models.CharField(
        max_length=255,
        choices=OrderStatus.choices,
        default=OrderStatus.PAYMENT_WAITING.value,
    )

    @property
    def is_paid(self) -> bool:
        return self.transactions.filter(
            status__in=(
                TransactionStatus.COMPLETED.value,
                TransactionStatus.PENDING.value,
            )
        ).exists()


class OrderCartItem(models.Model):
    """
    Individual items within an order, linking products with their ordered quantities.
    Forms the detail level of order composition.
    """

    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
