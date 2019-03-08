from rest_framework import serializers

from nad_app.models import ParkingType


class ParkingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingType
        fields = '__all__'
