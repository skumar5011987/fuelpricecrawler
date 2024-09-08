import time
from django.core.management import BaseCommand



class Command(BaseCommand):
    help = "This command crawls for cities and then the fuel price history from ndtv.com/fuel-prices"
    
    def handle(self, *args, **kwargs):
        from crawler.scripts.ndtv_crawler import (
            get_available_cities, parse_page_url, get_page_content, extract_fuelprice_history
        )
        from crawler.models.fuelprice import Location
        
        try:
            cities = get_available_cities()
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f"[Error]: Can't extract cities list."))
            return
        
        for city in cities:
            try:
                url = parse_page_url(city)
                self.stdout.write(self.style.SUCCESS(f"[Info]: Crawling '{url}'"))
                content = get_page_content(url)
                if content is None:
                    # can rescedule for this page url
                    continue
                
                data = extract_fuelprice_history(city, content)
                Location.create_data(data)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"[Error]: Crawling '{url}'"))
            
        self.stdout.write(self.style.SUCCESS("Completed"))