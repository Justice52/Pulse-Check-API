from django.urls import path

from .views import MonitorCreateView

urlpatterns = [
    path(
        "monitors", MonitorCreateView.as_view(), name="create-monitor"),
]