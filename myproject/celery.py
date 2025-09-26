import os
from dotenv import load_dotenv

load_dotenv()  # <-- load environment variables first
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

from celery import Celery
from celery.schedules import crontab

app = Celery("myproject")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "check-sizes-every-12-hours": {
        "task": "shop.tasks.update_sizes",
        "schedule": crontab(minute=0, hour="*/12"),  # runs at 0th minute, every 12 hours
    },
    "check-card-items-every-12-hours": {
        "task": "shop.tasks.remove_from_cart",
        "schedule": crontab(minute=0, hour="*/12"),  # runs at 0th minute, every 12 hours
    }
}