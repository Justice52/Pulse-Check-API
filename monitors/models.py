from django.db import models
from django.utils import timezone


class Monitor(models.Model):

    STATUS_CHOICES = [
        ("active", "Active"),
        ("paused", "Paused"),
        ("down", "Down"),
    ]

    device_id = models.CharField(
        max_length=100,
        unique=True
    )

    timeout = models.PositiveIntegerField()

    alert_email = models.EmailField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    last_heartbeat = models.DateTimeField(
        default=timezone.now
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.device_id
    
