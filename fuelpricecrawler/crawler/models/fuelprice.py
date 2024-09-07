from django.db import models

class Location(models.Model):
    state = models.CharField("State", max_length=255)
    city = models.CharField("City", max_length=255)
    
    def __str__(self):
        return f"{self.city}"
    
class FuelPrice(models.Model):
    
    city = models.ForeignKey(Location, related_name="fuel_prices", on_delete=models.CASCADE)
    fuel = models.CharField("Fuel", max_length=50, default='petrol')
    price = models.DecimalField("Price", max_digits=7, decimal_places=2)
    date = models.DateField("Date",)
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Fuel Prices"
        unique_together = ["city", "fuel", "date"]
    
    def __str__(self):
        return f"{self.city}"
    
