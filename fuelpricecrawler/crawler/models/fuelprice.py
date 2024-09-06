from django.db import models


class FuelPrice(models.Model):
    FUEL_CHOICES = (
        ("petrol", "Petrol"),
        ("diesel", "Diesel"),
    )
    
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    fuel = models.CharField(max_length=50, default='petrol', choices=FUEL_CHOICES)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ["state", "city"]
        verbose_name = "Fuel Price"
        verbose_name_plural = "Fuel Prices"
        unique_together = ["state", "city", "created_at"]
    
    def __str__(self):
        return f"{self.state}| {self.city} (Rs. {self.fuel})"
