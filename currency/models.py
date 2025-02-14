from django.db import models

from common.models import BaseModel


class Currency(BaseModel):
    name = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
