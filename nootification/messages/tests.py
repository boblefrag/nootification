from unittest.mock import Mock, patch
from urllib.parse import urljoin

from django.conf import settings
from django.test import TestCase

from .api import publish, send_notification


class MessageAPITestCase(TestCase):

    fixtures = ["initial_data.json"]

    @patch("django_rq.get_queue")
    def test_publish_success(self, mock_get_queue):
        """
        Should retrieve the alert, fetch recipients based on location and label,
        and create a task to send the notifiactions to each reevelant users.
        """
        mock_queue = Mock()
        mock_queue.enqueue = Mock()
        mock_get_queue.return_value = mock_queue

        publish(alert_id=1)

        called_args, called_kwargs = mock_queue.enqueue.call_args
        self.assertEqual(
            called_args[1],
            {
                "target_user_uuid": "00000000-0000-0000-0000-000000000002",
                "url": "https://example.com/alert/1",
                "alert_uuid": "00000000-0000-0000-0000-000000000001",
                "location": "Carrefour",
                "label": "Theft",
            },
        )

    @patch("requests.post")
    def test_send_notifications(self, mock_post):
        url = urljoin(settings.THIRD_SERVICE, "/webhook/notifications/")
        payload = {
            "target_user_uuid": "00000000-0000-0000-0000-000000000023",
            "url": "https://media.veesion.io/4d700130-9ce0-4abf-8266-6833edddab9b.mp4",
            "alert_uuid": "4d700130-9ce0-4abf-8266-6833edddab9b",
            "location": "Franprix",
            "label": "suspicious",
        }
        send_notification(payload)
        mock_post.assert_called_once_with(url, json=payload)
