from django.urls import path

from .views import HeartbeatView, MonitorCreateView

urlpatterns = [
    path("monitors", MonitorCreateView.as_view(), name="create-monitor"),
    path("monitors/<str:device_id>/heartbeat", HeartbeatView.as_view(), name="heartbeat"),

]