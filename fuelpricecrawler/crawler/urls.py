from django.urls import path, re_path
from crawler.views import (HomeAPIView, CrawlAPIView, ListCitiesAPIView, FuelPricesAPIView)

urlpatterns = [
    path("", HomeAPIView.as_view(), name="home"),
    path("list-cities", ListCitiesAPIView.as_view(), name="city list"),
    path("crawl-fuel-prices", CrawlAPIView.as_view(), name="crawl fuel prices"),
    path("fuel-price", FuelPricesAPIView.as_view(), name="fuel prices"),
]
