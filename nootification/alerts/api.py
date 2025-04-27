from rest_framework import serializers

from .models import Alert


class AlertSerializer(serializers.ModelSerializer):
    location = serializers.CharField(source="location.location", read_only=True)

    class Meta:
        model = Alert
        fields = ["url", "alert_uuid", "location", "label"]


def get_alert(alert_id):
    """
    Return a representation of alerts suitable for publishing
    """

    alert = Alert.objects.get(pk=alert_id)

    return AlertSerializer(alert).data
