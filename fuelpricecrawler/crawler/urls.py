from django.urls import path, re_path
from crawler.views import (HomeAPIView, CrawlAPIView, ListCitiesAPIView, FuelPricesAPIView)

urlpatterns = [
    path("", HomeAPIView.as_view(), name="home"),
    path("list-cities", ListCitiesAPIView.as_view(), name="city list"),
    path("crawl", CrawlAPIView.as_view(), name="crawler"),
    re_path(
        "fuel-price/(?P<city>[-\w]+)/(?P<state>.*)$",
        FuelPricesAPIView.as_view(),
        name="fuel prices"
    )
]
