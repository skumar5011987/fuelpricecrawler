from django.urls import path
from crawler.views import HomeAPIView

urlpatterns = [
    path("", HomeAPIView.as_view(), name="home"),
]
