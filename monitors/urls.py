from django.urls import path

from .views import HeartbeatView, MonitorCreateView, PauseMonitorView, MonitorListView, MonitorDetailView

urlpatterns = [
    path("monitors", MonitorCreateView.as_view(), name="create-monitor"),
    path("monitors/all", MonitorListView.as_view()),
    path("monitors/<str:device_id>/heartbeat", HeartbeatView.as_view(), name="heartbeat"),
    path("monitors/<str:device_id>/pause", PauseMonitorView.as_view(), name="pause-monitor"),
    path("monitors/<str:device_id>", MonitorDetailView.as_view()),


]