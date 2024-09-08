import time
import logging
from fuelpricecrawler.views import (BaseAPIView, APIResponse ,SUCCESS, FAIL,)
from crawler.scripts.ndtv_crawler import (
    get_available_cities, parse_page_url, extract_fuelprice_history, get_page_content
    )
from crawler.models.fuelprice import Location
from .serializers import LocationSerializer
from rest_framework import generics, views
from django.core.cache import cache

_logger = logging.getLogger(__name__)

class HomeAPIView(views.APIView):
    def get(self, request):
        return APIResponse(SUCCESS, message="Welcome, Check Petrol price for all states and cities in India.")

class ListCitiesAPIView(generics.ListAPIView):
    
    def get(self, request):
        cache_key = "cities"
        cities = cache.get(cache_key)
        if not cities:
            cities = list(Location.objects.all().values_list("city", flat=True))
            cache.set(cache_key, cities, timeout=6*60*60)
            
        return APIResponse(SUCCESS, message="Available cities", data=cities)
    
class FuelPricesAPIView(generics.ListAPIView):
    
    def get(self, request, city="", state=""):
        params = request.query_params.copy()
        city = " ".join(city.split("-")).title()
        if not city:
            return APIResponse(FAIL, message="Please provide city name.")
        
        cache_key = city
        data = cache.get(cache_key)
        if not data:
            
            qs = Location.objects.filter(city__iexact=city)
            if state:
                state = " ".join(state.split("-")).title()
                qs = qs.filter(state=state)
            
            data = LocationSerializer(qs, many=True).data
            cache.set(cache_key, data, timeout=6*60*60)
            
        return APIResponse(SUCCESS, data=data)


class CrawlAPIView(BaseAPIView):
    
    def post(self, request):
        
        try:
            cities = get_available_cities()
        except Exception as exc:
            _logger.error(f"Exception: {exc}")
            return APIResponse(FAIL)
        
        for city in cities:
            try:
                url = parse_page_url(city)
                
                _logger.error(f"[Info]: Crawling '{url}'")
                time.sleep(1)
                content = get_page_content(url)
                if content is None:
                    # can rescedule for this page url
                    continue
                
                data = extract_fuelprice_history(city, content)
                Location.create_data(data)
            except Exception as e:
                _logger.error(f"[Error]: Crawling '{url}'")
                
        
        return APIResponse(SUCCESS)