from rest_framework import serializers

from manuscript.models import Location


class ToponymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["country", "latitude", "longitude"]
