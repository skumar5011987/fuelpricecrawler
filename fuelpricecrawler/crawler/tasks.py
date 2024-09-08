import logging
import time
from fuelpricecrawler.celery import app
# from celery.signals import task_failure
from django.core.management import call_command

_logger = logging.getLogger(__name__)


# @task_failure.connect
# def handle_task_failure(**kwargs):
#     from traceback import format_tb

#     _logger.error(
#         "[task:%s:%s]"
#         % (
#             kwargs.get("task_id"),
#             kwargs["sender"].request.correlation_id,
#         )
#         + "\n"
#         + "".join(format_tb(kwargs.get("traceback", [])))
#         + "\n"
#         + str(kwargs.get("exception", ""))
#     )


@app.task
def run_ndtv_fuel_prices():
    call_command('ndtv_fuel_prices') 


@app.task(name="crawl_ndtv_fuelprices", max_retries=3, retry_backoff=True, rate_limit="300/m")
def crwal_ndtv_fuelprices(city=""):
    from crawler.models.fuelprice import Location
    from crawler.scripts.ndtv_crawler import (
        parse_page_url, extract_fuelprice_history, get_page_content
        )
    
    if not (city ):
        _logger.error(f"City name is required.")
        return
    
    try:
        url = parse_page_url(city)
        _logger.error(f"[Info]: Crawling '{url}'")
        time.sleep(1)
        content = get_page_content(url)
        
        data = extract_fuelprice_history(city, content)
        Location.create_data(data)
    except Exception as exc:
        _logger.exception(exc)
        crwal_ndtv_fuelprices.retry(countdown=10, exc=exc)