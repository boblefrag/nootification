"""
This module defines the API interface for internal communication between
different components of the project.
"""

from django.core.exceptions import ValidationError

from nootification.constants import LABEL, LEVEL

from .models import Company, StoreUser


def validate_company(value):
    """
    Validates that the provided value corresponds to the location of an existing Company.
    """
    try:
        company = Company.objects.get(location=value)
    except Company.DoesNotExist:
        raise ValidationError(f"No company found with location: {value}")
    return company


def get_location_recipients(location, label):
    """
    Returns recipients based on their preferences for alert level and location.
    """

    recipients = StoreUser.objects.filter(company__location=location)
    if label == LABEL.THEFT:
        recipients = recipients.filter(level__in=(LEVEL.CRITICAL, LEVEL.BOTH))
    else:
        recipients = recipients.filter(level__in=(LEVEL.STANDARD, LEVEL.BOTH))
    return list(recipients.values_list("user_uuid", flat=True))
