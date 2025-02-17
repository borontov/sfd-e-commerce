from django.db import models
from django.db.models import DecimalField

from common.models import BaseModel
from currency.models import Currency
from products.models import Product
from transactions.models import Transaction


class ProductPriceRecord(BaseModel):
    """
    Warning: Only created upon a successful transaction.
    Historical record of product prices at the time of successful transactions.
    Maintains price points, costs, and quantities for analytical purposes.
    """

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    price = DecimalField(max_digits=10, decimal_places=2)
    cost = DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    transaction = models.ForeignKey(
        Transaction,
        related_name="product_price_records",
        on_delete=models.PROTECT,
        null=True,
    )
