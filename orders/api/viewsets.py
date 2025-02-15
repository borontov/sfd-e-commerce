from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from orders.api.serializers import OrderSerializer
from orders.models import Order
from orders.tasks import cancel_order_task


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def cancel_order(self, request, pk=None):
        cancel_order_task.delay(pk)
        return Response(status=status.HTTP_200_OK)
