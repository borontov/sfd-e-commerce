from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from orders.api.serializers import OrderSerializer
from orders.business_logic.constants import OrderStatus
from orders.models import Order


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def cancel_order(self, request, pk=None):
        order = self.get_object()
        order.status = OrderStatus.CANCELLED
        order.save()
        return Response(status=status.HTTP_200_OK)

