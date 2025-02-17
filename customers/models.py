from django.db import models

from common.models import BaseModel


class Customer(BaseModel):
    """
    NOT USED IN CURRENT IMPLEMENTATION
    Core customer model storing essential user information and account balance.
    Acts as the primary model for customer-related operations.
    """

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class CustomerAddress(BaseModel):
    """
    NOT USED IN CURRENT IMPLEMENTATION
    Stores multiple addresses for customers with flags for shipping and billing purposes.
    Each customer can have multiple addresses with different roles.
    """

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="addresses"
    )
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=255)
    is_shipping_address = models.BooleanField(default=False)
    is_billing_address = models.BooleanField(default=False)


class CustomerPhone(BaseModel):
    """
    NOT USED IN CURRENT IMPLEMENTATION
    Manages customer phone numbers with verification status tracking.
    Supports multiple phone numbers per customer with primary number designation.
    """

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="phones"
    )
    country_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    is_primary = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(blank=True, null=True)
