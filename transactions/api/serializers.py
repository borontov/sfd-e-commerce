from rest_framework import serializers

from orders.models import Order
from transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    currency_name = serializers.CharField(max_length=3, required=False, default='USD', write_only=True)
    tax = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    product_price_records = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('status', 'currency')

    def get_product_price_records(self, obj):
        return obj.product_price_records.all().values()