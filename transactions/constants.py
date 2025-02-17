from django.db.models import TextChoices


class TransactionStatus(TextChoices):
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
