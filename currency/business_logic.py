from decimal import Decimal
from typing import Optional
from django.core.cache import cache


def get_currency_rate(*, currency_name: str) -> Optional[Decimal]:
    if currency_name != "USD":
        if cached_value := cache.get(f'CURRENCY_RATE_USD_{currency_name}'):
            currency_rate = Decimal(cached_value)
        else:
            return None
    else:
        currency_rate = Decimal(1)
    return currency_rate