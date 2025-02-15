import random
from decimal import Decimal

from django.core.cache import cache
from django.db.transaction import atomic
from rest_framework.viewsets import ModelViewSet

from transactions.api.serializers import TransactionSerializer
from transactions.constants import TransactionStatus
from transactions.models import Transaction
from rest_framework.exceptions import PermissionDenied

class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @atomic
    def perform_create(self, serializer):
        order = serializer.validated_data.get('order')
        if order.is_paid:
            raise PermissionDenied("Order is already paid")
        status = self._simulate_third_party_payment(serializer)
        amount_in_usd = serializer.validated_data.get('amount', 0)
        tax_in_usd = serializer.validated_data.get('tax', 0)
        currency_name = serializer.validated_data.pop('currency_name')
        if currency_name != "USD":
            currency_rate = Decimal(cache.get(f'CURRENCY_RATE_USD_{currency_name}'))
        else:
            currency_rate = Decimal(1)
        amount_in_currency = amount_in_usd * currency_rate
        tax_in_currency = tax_in_usd * currency_rate
        serializer.save(
            status=status,
            amount=amount_in_currency,
            tax=tax_in_currency
        )

    def _simulate_third_party_payment(self, serializer):
        return random.choice(TransactionStatus.values)


