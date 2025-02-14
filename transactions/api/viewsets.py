import random

from django.db.transaction import atomic
from rest_framework.viewsets import ModelViewSet

from transactions.api.serializers import TransactionSerializer
from transactions.constants import TransactionStatus
from transactions.models import Transaction


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        with atomic():
            # simulate a real transaction
            serializer.save(status=random.choice(TransactionStatus.values))
