from django.db import models

from common.models import BaseModel
from orders.business_logic.constants import OrderStatus
from transactions.constants import TransactionStatus


class Order(BaseModel):
    email = models.EmailField()
    products = models.ManyToManyField('products.Product')
    status = models.CharField(max_length=255, choices=OrderStatus.choices, default=OrderStatus.PAYMENT_WAITING)

    @property
    def is_paid(self) -> bool:
        return self.transactions.filter(
            status__in=(
                TransactionStatus.COMPLETED, TransactionStatus.PENDING
            ).exists()
        )
