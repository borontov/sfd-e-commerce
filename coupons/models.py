from django.db import models

from common.models import BaseModel


class Coupon(BaseModel):
    code = models.CharField(max_length=255, unique=True)
    discount_type = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    usage_left = models.PositiveIntegerField()
    active = models.BooleanField(default=True)
