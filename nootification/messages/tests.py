from unittest.mock import Mock, patch

from django.test import TestCase

from .api import publish


class PublishViewTestCase(TestCase):

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
