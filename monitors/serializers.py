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
    def validate_id(self, value):
        if Monitor.objects.filter(device_id=value).exists():
            raise serializers.ValidationError(
                "A monitor with this ID already exists."
            )
        return value

    def create(self, validated_data):
        return Monitor.objects.create(**validated_data)
    
  
    

class MonitorDetailSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="device_id", read_only=True)

    class Meta:
        model = Monitor
        fields = [
            "id",
            "timeout",
            "alert_email",
            "status",
            "last_heartbeat",
            "created_at",
        ]