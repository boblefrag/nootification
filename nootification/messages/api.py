import logging
from urllib.parse import urljoin

import django_rq
from alerts.api import get_alert
from django.conf import settings
from stores.api import get_location_recipients
from tenacity import retry, retry_if_not_exception_type, stop_after_attempt, wait_fixed

from .services import HttpMessageSender

logger = logging.getLogger("notifications")


class ClientError(Exception):
    """
    Catch all non-retriable errors (4xx)
    """


@retry(
    retry=retry_if_not_exception_type(ClientError),
    wait=wait_fixed(3),
    stop=stop_after_attempt(3),
)
def send_notification(payload):
    """
    Send notifications to third-party services. If a server error (5xx) occurs, retry the request
    up to three times with a 3-second wait between attempts.

    Retries are logged as warnings, and errors are logged as errors. In production, a monitoring
    system would alert us if repeated failures happen on the client webhook.
    """
    http_sender = HttpMessageSender(
        webhook_url=urljoin(settings.THIRD_SERVICE, "/webhook/notifications/")
    )
    http_sender.send_message(payload)


def publish(alert_id):
    queue = django_rq.get_queue("default")
    alert = get_alert(alert_id)
    recipients = get_location_recipients(alert["location"], alert["label"])
    logger.info(f"Recipients: {recipients}")
    for user_uuid in recipients:
        payload = {"target_user_uuid": str(user_uuid)}
        payload.update(alert)
        queue.enqueue(send_notification, payload)
