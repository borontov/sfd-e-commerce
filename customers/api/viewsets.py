from rest_framework.viewsets import ModelViewSet

from customers.api.serializers import CustomerSerializer, CustomerAddressSerializer, CustomerPhoneSerializer
from customers.models import Customer, CustomerAddress, CustomerPhone


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerAddressViewSet(ModelViewSet):
    queryset = CustomerAddress.objects.all()
    serializer_class = CustomerAddressSerializer


class CustomerPhoneViewSet(ModelViewSet):
    queryset = CustomerPhone.objects.all()
    serializer_class = CustomerPhoneSerializer
