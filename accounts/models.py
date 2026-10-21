import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Role(models.TextChoices):
        SUPER_ADMIN = "SA", "Super Admin"
        MANAGER = "M", "Manager"
        AGENT = "A", "Field Agent"
        PANCHAYATH = "P", "Panchayath User"

    role = models.CharField(
        max_length=2,
        choices=Role.choices,
        default=Role.AGENT,
    )

    def __str__(self):
        return self.get_full_name() or self.username