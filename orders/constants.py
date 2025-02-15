from django.db.models import TextChoices


class OrderStatus(TextChoices):
    PAYMENT_WAITING = 'payment_waiting', 'Payment Waiting'
    PROCESSING = 'processing', 'Processing'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'
