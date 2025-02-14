from rest_framework import serializers

from orders.models import Order
from transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('status', )
