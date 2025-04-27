from django.urls import path

from .views import UpdatePreferenceView

urlpatterns = [
    path("<uuid:user_uuid>", UpdatePreferenceView.as_view(), name="preferences-update"),
]
