
from django.contrib import admin
from crawler.models.fuelprice import Location, FuelPrice

class FuelPriceInline(admin.TabularInline):
    model = FuelPrice
    extra = 1

class LocationAdmin(admin.ModelAdmin):
    list_display = ['city', 'state']
    search_fields = ['city', 'state']
    inlines = [FuelPriceInline]

admin.site.register(Location, LocationAdmin)

class FuelPriceAdmin(admin.ModelAdmin):
    list_display = ['city', 'fuel', 'date', 'price']
    list_filter = ['city',]
    search_fields = ['city__city', "city__state",]
    ordering = ['-date']

admin.site.register(FuelPrice, FuelPriceAdmin)