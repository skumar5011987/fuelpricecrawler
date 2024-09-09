import logging
import time
from django.core.management import call_command

from fuelpricecrawler.celery import app


_logger = logging.getLogger(__name__)

@app.task
def ndtv_fuel_prices_command():
    try:
        call_command('ndtv_fuel_prices')
        
    except Exception as exc:
        _logger.exception(exc)
        ndtv_fuel_prices_command.retry(countdown=300, exc=exc)


@app.task(name="crwal_ndtv_fuelprices", max_retries=1, retry_backoff=True, rate_limit="300/m")
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