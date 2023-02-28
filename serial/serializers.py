from rest_framework.serializers import ModelSerializer
from serial.models import Season, Serial


class SerialSerializer(ModelSerializer):
    class Meta:
        model = Serial
        fields = "__all__"


class SeasonSerializer(ModelSerializer):
    class Meta:
        model = Season
        fields = "__all__"
