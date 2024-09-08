from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from celery.utils.log import get_task_logger


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fuelpricecrawler.settings')

app = Celery('fuelpricecrawler')
app.conf.enable_utc=False
app.conf.update(timezone='Asia/Kolkata')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()

# Celery Beat settings
app.conf.beat_schedule = {
    'ndtv_fuel_prices_daily': {
        'task': 'crawler.tasks.run_ndtv_fuel_prices',
        'schedule': crontab(hour=18, minute=4),
    },
}


