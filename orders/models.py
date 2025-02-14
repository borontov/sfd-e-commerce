from django.db import models

from common.models import BaseModel
from orders.business_logic.constants import OrderStatus


class Order(BaseModel):
    email = models.EmailField()
    products = models.ManyToManyField('products.Product')
    status = models.CharField(max_length=255, choices=OrderStatus.choices, default=OrderStatus.PAYMENT_WAITING)
