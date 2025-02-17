from django.db import models

from common.models import BaseModel
from transactions.constants import TransactionStatus


class Transaction(BaseModel):
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.PROTECT,
        related_name="transactions",
        null=False,
        blank=False,
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
    )
    status = models.CharField(
        choices=TransactionStatus.choices,
        max_length=255,
        null=True,
        blank=False,
    )
    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=False,
    )
    currency = models.ForeignKey(
        "currency.Currency",
        on_delete=models.PROTECT,
        null=True,
        blank=False,
    )
