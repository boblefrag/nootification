import django_rq
from django.db import models

from nootification.constants import LABEL


class Alert(models.Model):
    url = models.URLField(max_length=250)
    location = models.ForeignKey("stores.Company", on_delete=models.CASCADE)
    alert_uuid = models.UUIDField(unique=True)
    label = models.CharField(max_length=10, choices=LABEL)
    time_spotted = models.DateTimeField()

    def save(self, *args, **kwargs):
        from messages.api import publish

        super().save(*args, **kwargs)
        queue = django_rq.get_queue("default")
        queue.enqueue(publish, self.id)
