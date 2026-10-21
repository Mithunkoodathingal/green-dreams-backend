
import uuid

from django.db import models


class Panchayath(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=150)
    code = models.SlugField(max_length=50, unique=True)
    district = models.CharField(max_length=100, default="Kozhikode")
    state = models.CharField(max_length=100, default="Kerala")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Panchayaths"

    def __str__(self):
        return self.name


class Ward(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    panchayath = models.ForeignKey(
        Panchayath,
        on_delete=models.PROTECT,
        related_name="wards",
    )
    number = models.PositiveIntegerField()
    location_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["panchayath__name", "number"]
        constraints = [
            models.UniqueConstraint(
                fields=["panchayath", "number"],
                name="unique_ward_number_per_panchayath",
            ),
        ]

    def __str__(self):
        return (
            f"{self.panchayath.name} - "
            f"Ward {self.number}: {self.location_name}"
        )
