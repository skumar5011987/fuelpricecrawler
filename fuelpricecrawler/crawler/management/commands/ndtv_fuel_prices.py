from typing import Any
from django.core.management import BaseCommand



class Command(BaseCommand):
    help = "This command crawls the fuel prices from ndtv.com/fuel-prices"
    
    def handle(self, *args, **kwargs):
        from crawler.scripts.ndtv_crawler import get_available_cities
        from crawler.models.fuelprice import Location
        
        results = get_available_cities()
        Location.create_data(results)
        self.stdout.write(self.style.SUCCESS("Completed"))