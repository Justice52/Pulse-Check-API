from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Monitor

from .serializers import MonitorSerializer, MonitorDetailSerializer


class MonitorCreateView(APIView):
    """Create a new device."""

    def post(self, request):

        serializer = MonitorSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Device created successfully."
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    

class HeartbeatView(APIView):
    """Send a heartbeat for a specific device."""

    def post(self, request, device_id):

        monitor = get_object_or_404(
            Monitor,
            device_id=device_id
        )

        if monitor.status == "down":
            return Response(
                {
                    "message": "Device is down."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        monitor.last_heartbeat = timezone.now()

        if monitor.status == "paused":
            monitor.status = "active"

        monitor.save()

        return Response(
        {
            "message": "I'm alive.",
            "device_id": monitor.device_id,
            "status": monitor.status,
            "last_heartbeat": monitor.last_heartbeat,
        },
        status=status.HTTP_200_OK,
    )


class PauseMonitorView(APIView):
    """Pauses a device."""
    def post(self, request, device_id):

        monitor = get_object_or_404(
            Monitor,
            device_id=device_id
        )

        if monitor.status == "down":
            return Response(
                {
                    "message": "Cannot pause a device that is already down."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if monitor.status == "paused":
            return Response(
                {
                    "message": "Device is already paused."
                },
                status=status.HTTP_200_OK
            )

        monitor.status = "paused"
        monitor.save()

        return Response(
            {
                "message": "Monitor paused successfully.",
                "status": monitor.status
            },
            status=status.HTTP_200_OK
        )


class MonitorListView(APIView):
    """Developer's Choice: List all monitors with details."""

    def get(self, request):

        monitors = Monitor.objects.all().order_by("-created_at")

        serializer = MonitorDetailSerializer(
            monitors,
            many=True
        )

        return Response(serializer.data)
    

    

class MonitorDetailView(APIView):
    """Developer's Choice: Get details of a specific monitor."""

    def get(self, request, device_id):

        monitor = get_object_or_404(
            Monitor,
            device_id=device_id
        )

        serializer = MonitorDetailSerializer(monitor)

        return Response(serializer.data)
    