from django.utils import timezone
from .models import Monitor



def check_monitors():
    """
    Check the status of all monitors and update their status if they have expired.
    """
    now = timezone.now()
    monitors = Monitor.objects.filter(status="active")

    for monitor in monitors:

        elasped_time = (
            now - monitor.last_heartbeat
        ).total_seconds()

        if elasped_time >= monitor.timeout:
            monitor.status = "down"
            monitor.save()

            print(
                {
                    "ALERT": f"Device {monitor.device_id} is down!",
                    "time": now.isoformat(),
                    "last_heartbeat": monitor.last_heartbeat,
                }
            )
