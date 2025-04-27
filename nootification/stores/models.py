# Create your models here.
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from nootification.constants import LEVEL


class Company(models.Model):
    location = models.CharField(max_length=255)


class StoreUser(AbstractUser):
    user_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="employees",
    )

    level = models.CharField(max_length=10, choices=LEVEL, default=LEVEL.CRITICAL)
