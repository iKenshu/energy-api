from rest_framework import serializers

from .models import Energy


class EnergySerializer(serializers.ModelSerializer):
    meter_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    
    class Meta:
        model = Energy
        fields = ["meter_date", "active_energy"]
