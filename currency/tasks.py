import logging
import random
from decimal import Decimal

from celery import shared_task
from django.core.cache import cache

from currency.constants import CurrencyName

logger = logging.getLogger(__name__)


@shared_task
def refresh_currency_rates():
    for currency_name in CurrencyName.values:
        if currency_name == "USD":
            continue
        new_value = Decimal(random.randint(0, 150) / 100)
        cache.set(f"CURRENCY_RATE_USD_{currency_name}", str(new_value))
        logger.info(
            f"Currency rate for {currency_name} updated to {new_value}"
        )
