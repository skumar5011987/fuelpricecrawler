from rest_framework import serializers
from crawler.models.fuelprice import Location, FuelPrice

class FuelPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelPrice
        fields = ['date', 'fuel', 'price']

class LocationSerializer(serializers.ModelSerializer):
    data = FuelPriceSerializer(source='fuel_prices', many=True)

    class Meta:
        model = Location
        fields = ['city', 'state', 'data']

    def create_fuelprice(self, validated_data):
        
        city_data = validated_data.get('city')
        state_data = validated_data.get('state')
        fuelprices = validated_data.get('fuel_prices')
        
        city_obj, created = Location.objects.get_or_create(
            city=city_data,
            state=state_data
        )
        
        for fuelprice in fuelprices:
            FuelPrice.objects.get_or_create(
                city=city_obj,
                fuel=fuelprice['fuel'],
                date=fuelprice['date'],
                defaults={'price': fuelprice['price']}
            )
        
        return city_obj
