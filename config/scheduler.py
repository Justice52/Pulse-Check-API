from apscheduler.schedulers.background import BackgroundScheduler

from monitors.services import check_monitors


def start_scheduler():
    """
    Start the background scheduler to check monitors every 5 seconds.
    """
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        check_monitors,
        "interval",
        seconds=5,
        id="monitor_checker",
        replace_existing=True
    )

    scheduler.start()

    print("Scheduler started. Monitoring devices every 5 seconds.")