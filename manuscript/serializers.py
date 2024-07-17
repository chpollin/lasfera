from rest_framework import serializers

from manuscript.models import Location


class ToponymSerializer(serializers.ModelSerializer):
    detailed_toponym = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ["id", "country", "latitude", "longitude", "detailed_toponym"]

    def get_detailed_toponym(self, obj):
        return {
            "id": obj.id,
            "country": obj.country,
            "latitude": obj.latitude,
            "longitude": obj.longitude,
        }
