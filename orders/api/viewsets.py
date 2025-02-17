from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from common.serializers import EmptySerializer
from orders.api.serializers import OrderCartItemSerializer, OrderSerializer
from orders.constants import OrderStatus
from orders.models import Order, OrderCartItem
from orders.tasks import cancel_order_task


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(
        detail=True,
        methods=["post"],
        url_path="cancel",
        serializer_class=EmptySerializer,
    )
    def cancel_order(self, request, pk=None):
        order = self.get_object()
        if order.status == OrderStatus.PROCESSING.value:
            cancel_order_task.delay(order_id=pk)
            return Response(status=status.HTTP_200_OK)
        raise PermissionDenied("Order can't be cancelled")


class OrderCartItemViewSet(ModelViewSet):
    queryset = OrderCartItem.objects.all()
    serializer_class = OrderCartItemSerializer
