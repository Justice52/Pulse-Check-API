from rest_framework import serializers
from .models import Monitor


class MonitorSerializer(serializers.ModelSerializer):
    # The API expects "id", but our model field is "device_id"
    id = serializers.CharField(source="device_id")

    class Meta:
        model = Monitor
        fields = [
            "id",
            "timeout",
            "alert_email",
        ]

    def create(self, validated_data):
        return Monitor.objects.create(**validated_data)