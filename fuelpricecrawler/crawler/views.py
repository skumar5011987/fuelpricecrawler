from fuelpricecrawler.views import (BaseAPIView, APIResponse ,SUCCESS, FAIL,)
from crawler.scripts.ndtv_crawler import crawl_fuelprices
from crawler.models.fuelprice import Location
from .serializers import LocationSerializer
from rest_framework import generics, views
from django.core.cache import cache

class HomeAPIView(views.APIView):
    def get(self, request):
        return APIResponse(SUCCESS, message="Welcome, Check Petrol price for all states and cities in India.")

class ListCitiesAPIView(generics.ListAPIView):
    
    def get(self, request):
        cities = list(Location.objects.all().values_list("city", flat=True))
        return APIResponse(SUCCESS, message="Available cities", data=cities)
    
class FuelPricesAPIView(generics.ListAPIView):
    
    def get(self, request, city="", state=""):
        params = request.query_params.copy()
        city = " ".join(city.split("-")).title()
        if not city:
            return APIResponse(FAIL, message="Please provide city name.")
        
        qs = Location.objects.filter(city__iexact=city)
        if state:
            state = " ".join(state.split("-")).title()
            qs = qs.filter(state=state)
        
        serializer = LocationSerializer(qs, many=True)        
        return APIResponse(SUCCESS, data=serializer.data)


class CrawlAPIView(BaseAPIView):
    
    def post(self, request):
        
        try:
            results = crawl_fuelprices()
            for rec in results:
                serializer = LocationSerializer(data=rec)
                if serializer.is_valid():
                    obj = serializer.create_fuelprice(serializer.validated_data)
            return APIResponse(SUCCESS)
        except Exception as e:
            print(f"Error while crawling: error msg: {e}")
            return APIResponse(FAIL)