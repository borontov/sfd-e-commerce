import random

from django.db.transaction import atomic
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

from currency.business_logic import get_currency_rate
from currency.models import Currency
from transactions.api.serializers import TransactionSerializer
from transactions.constants import TransactionStatus
from transactions.models import Transaction


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @atomic
    def perform_create(self, serializer: TransactionSerializer) -> None:
        order = serializer.validated_data.get("order")
        if order.is_paid:
            raise PermissionDenied("Order is already paid")
        status = self._simulate_third_party_payment()
        currency_name = serializer.validated_data.pop("currency_name")
        currency_rate = get_currency_rate(currency_name=currency_name)
        currency = Currency.objects.create(
            name=currency_name,
            rate=currency_rate,
        )
        amount_in_currency = (
            serializer.validated_data.pop("amount_in_usd", 0) * currency.rate
        )
        tax_in_currency = (
            serializer.validated_data.pop("tax_in_usd", 0) * currency.rate
        )
        serializer.save(
            status=status,
            amount=amount_in_currency,
            tax=tax_in_currency,
            currency=currency,
        )

    def _simulate_third_party_payment(self) -> str:
        return random.choice(TransactionStatus.values)
