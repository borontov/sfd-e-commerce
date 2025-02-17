from django.db import models

from common.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    stock = models.PositiveIntegerField(
        default=0,
    )
