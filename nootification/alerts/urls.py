from django.urls import path

from .views import WebhookView

urlpatterns = [
    path("alerts", WebhookView.as_view(), name="alert-webhook"),
]
