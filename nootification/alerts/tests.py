from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Alert

ALERT_PAYLOAD = {
    "url": "https://media.veesion.io/b36006d7-adfa-4f3c-a56c-addcb4e4f95d.mp4",
    "location": "Carrefour",
    "alert_uuid": "33cbb18c-3e9d-4acc-9667-2fbe7bf29137",
    "label": "theft",
    "time_spotted": 1742470260.083,
}


class WebhookViewTest(APITestCase):
    """
    Tests the WebhookView to ensure an alert can be created successfully via the API.
    """

    fixtures = ["initial_data.json"]

    def test_create_alert_success(self):
        """
        Should create a new alert and return HTTP 201 when valid data is posted.
        """

        url = reverse("alert-webhook")
        response = self.client.post(url, ALERT_PAYLOAD, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Alert.objects.filter(alert_uuid=ALERT_PAYLOAD["alert_uuid"]).exists()
        )
