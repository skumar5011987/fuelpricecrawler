import time
import logging
from fuelpricecrawler.views import (BaseAPIView, APIResponse ,SUCCESS, FAIL,)
from crawler.scripts.ndtv_crawler import (
    get_available_cities, parse_page_url, extract_fuelprice_history, get_page_content
    )
from rest_framework import generics, views
from django.core.cache import cache

_logger = logging.getLogger(__name__)

class HomeAPIView(views.APIView):
    def get(self, request):
        return APIResponse(SUCCESS, message="Welcome, Check Petrol price for all states and cities in India.")

class ListCitiesAPIView(generics.ListAPIView):
    
    def get(self, request):
        from crawler.models.fuelprice import Location
        
        cache_key = "cities"
        cities = cache.get(cache_key)
        if not cities:
            cities = list(Location.objects.all().values_list("city", flat=True))
            cache.set(cache_key, cities, timeout=6*60*60)
            
        return APIResponse(SUCCESS, message="Available cities", data=cities)
    
class FuelPricesAPIView(generics.ListAPIView):
    
    def get(self, request):
        from crawler.models.fuelprice import Location
        from .serializers import LocationSerializer
        
        params = request.query_params.copy()
        city, state = params.get("city",""), params.get("state","")
        city, state = " ".join(city.split("-")).title(), " ".join(state.split("-")).title()
        if not city:
            return APIResponse(FAIL, message="Please provide city name.")
        
        cache_key = city
        data = cache.get(cache_key)
        if not data:
            
            qs = Location.objects.filter(city__iexact=city)
            if state:
                qs = qs.filter(state=state)
            
            data = LocationSerializer(qs, many=True).data
            cache.set(cache_key, data, timeout=3*60*60)
            
        return APIResponse(SUCCESS, data=data)
