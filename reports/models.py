from django.db import models

from common.models import BaseModel


class Report(BaseModel):
    start_date = models.DateField()
    end_date = models.DateField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_units_sold = models.IntegerField()
    number_of_returns = models.IntegerField()
