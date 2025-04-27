"""
Define project wide constants
"""

from django.db import models


class LABEL(models.TextChoices):
    THEFT = "theft", "Theft"
    SUSPICIOUS = "suspicious", "Suspicious"
    NORMAL = "normal", "Normal"


class LEVEL(models.TextChoices):
    CRITICAL = "critical", "Critical"
    STANDARD = "standard", "Standard"
    BOTH = "both", "Both"
