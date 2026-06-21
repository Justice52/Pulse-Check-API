from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Monitor

from .serializers import MonitorSerializer


class MonitorCreateView(APIView):

    def post(self, request):

        serializer = MonitorSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Monitor created successfully."
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    

class HeartbeatView(APIView):

    def post(self, request, device_id):

        monitor = get_object_or_404(
            Monitor,
            device_id=device_id
        )

        if monitor.status == "down":
            return Response(
                {
                    "message": "Monitor has already expired."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        monitor.last_heartbeat = timezone.now()

        if monitor.status == "paused":
            monitor.status = "active"

        monitor.save()

        return Response(
            {
                "message": "Heartbeat received."
            },
            status=status.HTTP_200_OK
        )