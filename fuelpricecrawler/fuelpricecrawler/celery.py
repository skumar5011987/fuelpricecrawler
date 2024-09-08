
import os
import time
from django.conf import settings
from celery import Celery
from celery.signals import task_failure
from celery.utils.log import get_task_logger

from crawler.scripts.ndtv_crawler import (
    parse_page_url, extract_fuelprice_history, get_page_content
    )
from crawler.models.fuelprice import Location


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fuelpricecrawler.settings')
_logger = get_task_logger(__name__)

app = Celery('fuelpricecrawler')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@task_failure.connect
def handle_task_failure(**kwargs):
    from traceback import format_tb

    _logger.error(
        "[task:%s:%s]"
        % (
            kwargs.get("task_id"),
            kwargs["sender"].request.correlation_id,
        )
        + "\n"
        + "".join(format_tb(kwargs.get("traceback", [])))
        + "\n"
        + str(kwargs.get("exception", ""))
    )


@app.task(name="crawl_fuelprices", max_retries=3, retry_backoff=True, rate_limit="300/m")
def crwal_fuelprices(city="", page_url=""):
    
    if not (city ):
        _logger.error(f"City name is required.")
        return
    
    try:
        if not page_url:
            url = parse_page_url(city)
        
        _logger.error(f"[Info]: Crawling '{url}'")
        time.sleep(1)
        content = get_page_content(url)
        
        data = extract_fuelprice_history(city, content)
        Location.create_data(data)
    except Exception as exc:
        _logger.exception(exc)
        crwal_fuelprices.retry(countdown=10, exc=exc)
    

