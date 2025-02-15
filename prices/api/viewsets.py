from rest_framework.viewsets import ModelViewSet

from prices.api.serializers import ProductPriceRecordSerializer
from prices.models import ProductPriceRecord


class ProductPriceRecordViewSet(ModelViewSet):
    queryset = ProductPriceRecord.objects.all()
    serializer_class = ProductPriceRecordSerializer
