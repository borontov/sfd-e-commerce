from datetime import timedelta

from celery import shared_task
from django.db.models import Sum, F, DecimalField
from django.db.transaction import atomic

from orders.business_logic.constants import OrderStatus
from orders.models import Order
from prices.models import ProductPriceRecord
from reports.models import Report
from django.utils import timezone
import logging

from transactions.constants import TransactionStatus

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def generate_report(self) -> None:
    """
    Generate a summary report for a selected time period, including:
    ▪ Total revenue
    ▪ Profit
    ▪ Number of units sold
    ▪ Number of returns
    """
    try:
        with atomic():
            today = timezone.now().date()
            start_date = today - timedelta(days=7)
            end_date = today

            aggregator = (
                ProductPriceRecord.objects
                .filter(
                    created_at__range=[start_date, end_date],
                    transaction__status=TransactionStatus.COMPLETED,
                )
                .aggregate(
                    total_revenue=Sum(
                        F("price") * F("quantity"),
                        output_field=DecimalField(max_digits=20, decimal_places=2)
                    ),
                    total_cost=Sum(
                        F("cost") * F("quantity"),
                        output_field=DecimalField(max_digits=20, decimal_places=2)
                    ),
                    number_of_units_sold=Sum("quantity")
                )
            )
            total_revenue = aggregator["total_revenue"] or 0
            total_cost = aggregator["total_cost"] or 0
            number_of_units_sold = aggregator["number_of_units_sold"] or 0

            number_of_returns = Order.objects.filter(
                created_at__range=[start_date, end_date],
                status=OrderStatus.CANCELLED
            ).count()

            profit = total_revenue - total_cost

            Report.objects.create(
                start_date=start_date,
                end_date=end_date,
                total_revenue=total_revenue,
                profit=profit,
                number_of_units_sold=number_of_units_sold,
                number_of_returns=number_of_returns,
            )
    except Exception as exc:
        logger.error(f"Failed to generate report: {exc}")
        raise self.retry(exc=exc)

