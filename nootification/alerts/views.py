import datetime

from rest_framework import serializers
from rest_framework.generics import CreateAPIView
from stores.api import validate_company

from .models import Alert


class AlertSerializer(serializers.ModelSerializer):

    location = serializers.CharField(write_only=True)
    time_spotted = serializers.FloatField(write_only=True)

    class Meta:
        model = Alert
        fields = ("url", "location", "alert_uuid", "label", "time_spotted")

    def validate_location(self, value):
        return validate_company(value)

    def create(self, validated_data):
        location = validated_data.pop("location")
        validated_data["location"] = location

        timestamp = validated_data.pop("time_spotted")
        validated_data["time_spotted"] = datetime.datetime.fromtimestamp(timestamp)

        return super().create(validated_data)


class WebhookView(CreateAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    lookup_field = "alert_uuid"
