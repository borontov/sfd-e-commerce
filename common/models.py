from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model providing common fields for all models:
    timestamps for creation, updates and soft deletion, plus optional notes.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)  # soft delete
    notes = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
