import uuid

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from nootification.constants import LABEL, LEVEL

from .api import get_location_recipients, validate_company
from .models import StoreUser


class PreferencesViewTest(TestCase):
    fixtures = ["initial_data.json"]

    def test_preferences_change(self):
        """
        Tests the user preferences functionality, ensuring that valid
        preferences are correctly saved and that expected validation
        errors are properly handled in nominal cases.
        """
        # Test preferences are saved
        payload = {"level": "critical"}
        user = StoreUser.objects.first()
        url = reverse("preferences-update", args=[user.user_uuid])
        response = self.client.patch(url, data=payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["level"], "critical")

        user.refresh_from_db()
        self.assertEqual(user.level, "critical")
        payload["level"] = "standard"
        response = self.client.patch(url, data=payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["level"], "standard")

        # Test common validations errors

        url = reverse("preferences-update", args=[str(uuid.uuid4())])
        response = self.client.patch(url, data=payload, content_type="application/json")
        self.assertEqual(response.status_code, 404)

        url = reverse("preferences-update", args=[user.user_uuid])
        response = self.client.patch(
            url, data={"level": "Zelda"}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json(), {"level": ['"Zelda" is not a valid choice.']})


class APITest(TestCase):
    """
    This test suite verifies the API that other modules will use.

    Following the idea that tests are a form of documentation,
    these tests not only ensure correctness
    but also demonstrate how the API is meant to be used.
    """

    fixtures = ["initial_data.json"]

    def test_valid_location(self):
        """Should return the company when location is valid."""
        company = validate_company("Carrefour")
        self.assertEqual(company.location, "Carrefour")

    def test_invalid_location(self):
        """Should raise ValidationError when location does not match any company."""
        with self.assertRaises(ValidationError):
            validate_company("Apple")

    def test_theft_label_filters_critical_and_both(self):
        """Returns only users with CRITICAL or BOTH level for THEFT label."""
        recipients = get_location_recipients("Carrefour", LABEL.THEFT)

        users = StoreUser.objects.filter(user_uuid__in=recipients)

        self.assertTrue(
            all(user.level in [LEVEL.CRITICAL, LEVEL.BOTH] for user in users)
        )

    def test_other_label_filters_standard_and_both(self):
        """Returns only users with STANDARD or BOTH level for non-THEFT labels."""
        recipients = get_location_recipients("Carrefour", LABEL.SUSPICIOUS)
        users = StoreUser.objects.filter(user_uuid__in=recipients)
        self.assertTrue(
            all(user.level in [LEVEL.STANDARD, LEVEL.BOTH] for user in users)
        )
