import logging
from datetime import datetime

from celery import shared_task
from django.db.models import DecimalField, F, Sum
from django.db.transaction import atomic

from orders.constants import OrderStatus
from orders.models import Order
from prices.models import ProductPriceRecord
from reports.models import Report

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
@atomic  # atomic is used to ensure that all operations are committed or rolled back as a whole
def generate_report(self, start_date: str, end_date: str) -> None:
    """
    Generate a summary report for a selected time period, including:
    ▪ Total revenue
    ▪ Profit
    ▪ Number of units sold
    ▪ Number of returns
    """
    try:
        parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        aggregator = ProductPriceRecord.objects.filter(
            created_at__range=[parsed_start_date, parsed_end_date],
        ).aggregate(
            total_revenue=Sum(
                F("price") * F("quantity") / F("currency__rate"),
                output_field=DecimalField(max_digits=20, decimal_places=2),
            ),
            total_cost=Sum(
                F("cost") * F("quantity") / F("currency__rate"),
                output_field=DecimalField(max_digits=20, decimal_places=2),
            ),
            number_of_units_sold=Sum("quantity"),
        )
        total_revenue = aggregator["total_revenue"] or 0
        total_cost = aggregator["total_cost"] or 0
        number_of_units_sold = aggregator["number_of_units_sold"] or 0

        number_of_returns = Order.objects.filter(
            created_at__range=[parsed_start_date, parsed_end_date],
            status=OrderStatus.CANCELLED.value,
        ).count()

        profit = total_revenue - total_cost

        Report.objects.create(
            start_date=parsed_start_date,
            end_date=parsed_end_date,
            total_revenue=total_revenue,
            profit=profit,
            number_of_units_sold=number_of_units_sold,
            number_of_returns=number_of_returns,
        )
    except Exception as exc:
        logger.error(f"Failed to generate report: {exc}")
        raise self.retry(exc=exc)
