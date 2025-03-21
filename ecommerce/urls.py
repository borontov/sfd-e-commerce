from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from customers.api.viewsets import (
    CustomerAddressViewSet,
    CustomerPhoneViewSet,
    CustomerViewSet,
)
from ecommerce import settings
from orders.api.viewsets import OrderCartItemViewSet, OrderViewSet
from prices.api.viewsets import ProductPriceRecordViewSet
from products.api.viewsets import ProductViewSet
from reports.api.viewsets import ReportViewSet
from transactions.api.viewsets import TransactionViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Simplified E-commerce API",
        default_version="v1",
        description="Minimal API for E-commerce",
        contact=openapi.Contact(email="anborontov@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
router_v1 = routers.DefaultRouter()

router_v1.register(r"orders", OrderViewSet)
router_v1.register(r"products", ProductViewSet)
router_v1.register(r"transactions", TransactionViewSet)
router_v1.register(r"customers", CustomerViewSet)
router_v1.register(r"customers/addresses", CustomerAddressViewSet)
router_v1.register(r"customers/phones", CustomerPhoneViewSet)
router_v1.register(r"product_price_records", ProductPriceRecordViewSet)
router_v1.register(r"order_cart_items", OrderCartItemViewSet)
router_v1.register(r"reports", ReportViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router_v1.urls)),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
