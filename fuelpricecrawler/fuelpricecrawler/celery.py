from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

from celery.signals import task_failure
from celery.utils.log import get_task_logger


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fuelpricecrawler.settings')
_logger = get_task_logger(__name__)

app = Celery('fuelpricecrawler')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# Schedule management command
app.conf.beat_schedule = {
    'ndtv_fuel_prices_daily': {
        'task': 'crawler.tasks.ndtv_fuel_prices_command',
        'schedule': crontab(hour=7, minute=30),
    }
}

@task_failure.connect
def handle_task_failure(sender=None, task_id=None, exception=None, traceback=None, **kwargs):
    from traceback import format_tb
    
    if isinstance(traceback, str):
        formatted_traceback = traceback
    else:
        formatted_traceback = "".join(format_tb(traceback))
    
    _logger.error(
        "[task:%s:%s]"
        % (
            task_id,
            sender.request.correlation_id if hasattr(sender.request, 'correlation_id') else 'N/A',
        )
        + "\n"
        + formatted_traceback
        + "\n"
        + str(exception or "No Exception")
    )
