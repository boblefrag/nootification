"""Manage the services used to send messages"""

import logging
from abc import ABC, abstractmethod

import requests  # type: ignore
from tenacity import retry, retry_if_not_exception_type, stop_after_attempt, wait_fixed

logger = logging.getLogger("notifications")


class ClientError(Exception):
    """
    Catch all non-retriable errors (4xx)
    """


class MessageSender(ABC):
    """
    Base class to send messages. Specific implementations should provide their
    own logic for sending messages (HTTP, Email, SMS).
    """

    @retry(
        retry=retry_if_not_exception_type(ClientError),
        wait=wait_fixed(3),
        stop=stop_after_attempt(3),
    )
    @abstractmethod
    def send_message(self, message):
        pass


class HttpMessageSender(MessageSender):

    def __init__(self, webhook_url):
        self.url = webhook_url

    def send_message(self, message):

        try:
            response = requests.post(self.url, json=message)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.warn(f"HTTPError while sending notification: {e}")
            if 400 <= e.response.status_code < 500:
                logger.error(f"HTTPError while sending notification: {e}")
                raise ClientError(e)
            else:
                raise
