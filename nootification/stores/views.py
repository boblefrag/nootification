from rest_framework import serializers
from rest_framework.generics import UpdateAPIView

from .models import StoreUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreUser
        fields = ["level"]


class UpdatePreferenceView(UpdateAPIView):
    queryset = StoreUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = "user_uuid"
