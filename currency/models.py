from django.db import models

from common.models import BaseModel


class Currency(BaseModel):
    """
    Defines available currencies and their exchange rates.
    Used for multi-currency support across transactions and pricing.
    """

    name = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
