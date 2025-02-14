from rest_framework import serializers

from orders.models import Order
from products.models import Product


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        many=True
    )

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('status', )