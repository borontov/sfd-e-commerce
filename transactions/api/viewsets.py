import random

from django.db.transaction import atomic
from rest_framework.viewsets import ModelViewSet

from transactions.api.serializers import TransactionSerializer
from transactions.constants import TransactionStatus
from transactions.models import Transaction
from rest_framework.exceptions import PermissionDenied

class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        order = serializer.validated_data.get('order')
        if order.is_paid:
            raise PermissionDenied("Order is already paid")
        with atomic():
            # simulate a real transaction
            serializer.save(status=random.choice(TransactionStatus.values))
