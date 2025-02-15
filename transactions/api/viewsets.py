import random
from decimal import Decimal

from django.core.cache import cache
from django.db.transaction import atomic
from rest_framework.viewsets import ModelViewSet

from currency.models import Currency
from transactions.api.serializers import TransactionSerializer
from transactions.constants import TransactionStatus
from transactions.models import Transaction
from rest_framework.exceptions import PermissionDenied

class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @atomic
    def perform_create(self, serializer: TransactionSerializer) -> None:
        order = serializer.validated_data.get('order')
        if order.is_paid:
            raise PermissionDenied("Order is already paid")
        status = self._simulate_third_party_payment()
        currency = self._create_currency_instance(serializer=serializer)
        amount_in_currency = self._calculate_amount(currency=currency, serializer=serializer)
        tax_in_currency = self._calculate_tax(currency=currency, serializer=serializer)
        serializer.save(
            status=status,
            amount=amount_in_currency,
            tax=tax_in_currency,
            currency=currency,
        )

    def _calculate_tax(self, *, currency: Currency, serializer: TransactionSerializer) -> Decimal:
        tax_in_usd = serializer.validated_data.pop('tax_in_usd', 0)
        tax_in_currency = tax_in_usd * currency.rate
        return tax_in_currency

    def _calculate_amount(self, *, currency: Currency, serializer: TransactionSerializer) -> Decimal:
        amount_in_usd = serializer.validated_data.pop('amount_in_usd', 0)
        amount_in_currency = amount_in_usd * currency.rate
        return amount_in_currency

    def _create_currency_instance(self, *, serializer: TransactionSerializer) -> Currency:
        currency_name = serializer.validated_data.pop('currency_name')
        if currency_name != "USD":
            currency_rate = Decimal(cache.get(f'CURRENCY_RATE_USD_{currency_name}'))
        else:
            currency_rate = Decimal(1)
        return Currency.objects.create(
            name=currency_name,
            rate=currency_rate,
        )

    def _simulate_third_party_payment(self) -> str:
        return random.choice(TransactionStatus.values)


