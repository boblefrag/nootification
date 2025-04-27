from django.urls import include, path

urlpatterns = [
    path("preferences/", include("stores.urls")),
    path("webhooks/", include("alerts.urls")),
]
