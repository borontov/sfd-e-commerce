from rest_framework import serializers

from orders.models import Order
from transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    currency_name = serializers.CharField(
        max_length=3, required=False, default="USD", write_only=True
    )
    product_price_records = serializers.SerializerMethodField(read_only=True)
    currency = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = ("status", "currency", "tax", "amount")

    def get_product_price_records(self, obj):
        return obj.product_price_records.all().values()

    def get_currency(self, obj):
        if obj.currency:
            return {"name": obj.currency.name, "rate": obj.currency.rate}
        return None
