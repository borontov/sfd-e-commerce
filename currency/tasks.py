import random
from decimal import Decimal

from celery import shared_task
from django.core.cache import cache

from currency.constants import CurrencyName


@shared_task
def refresh_currency_rates():
    for currency in CurrencyName.values():
        if currency.name == 'USD':
            continue
        new_value = Decimal(random.randint(0, 150) / 100)
        cache.set(f"CURRENCY_RATE_USD_{currency.name}", str(new_value))
