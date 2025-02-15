from rest_framework import serializers

from orders.models import Order, OrderCartItem
from products.models import Product
from transactions.api.serializers import TransactionSerializer


class OrderCartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = OrderCartItem
        fields = '__all__'
        read_only_fields = ('order', )


class OrderSerializer(serializers.ModelSerializer):
    cart_items_list = OrderCartItemSerializer(many=True, write_only=True)
    email = serializers.EmailField(required=True)
    transaction = serializers.SerializerMethodField(read_only=True)
    cart_items = OrderCartItemSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('status', 'cart_items')

    def create(self, validated_data):
        cart_items_data = validated_data.pop('cart_items_list', [])
        order = Order.objects.create(**validated_data)
        for cart_item_data in cart_items_data:
            order.cart_items.add(
                OrderCartItem.objects.create(**cart_item_data)
            )
        return order

    def get_transaction(self, obj):
        return TransactionSerializer(
            instance=obj.transactions.order_by('-created_at').first(),
        ).data