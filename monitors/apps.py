import os
from django.apps import AppConfig


class MonitorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitors'

    def ready(self):
        """
        Start the scheduler when the app is ready.
        """
        if os.environ.get("RUN_MAIN") != "true":
            return  # Prevents the scheduler from starting twice in development
        
        from config.scheduler import start_scheduler
        start_scheduler()
