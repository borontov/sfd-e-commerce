from django.db.models import TextChoices


class CurrencyName(TextChoices):
    USD = "USD", "American Dollar"
    SGD = "SGD", "Singapore Dollar"
    EUR = "EUR", "Euro"
