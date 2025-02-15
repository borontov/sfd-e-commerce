from rest_framework import serializers

from prices.models import ProductPriceRecord


class ProductPriceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPriceRecord
        fields = '__all__'
