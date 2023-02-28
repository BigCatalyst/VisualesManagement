from offer.models import Offer
from rest_framework.serializers import ModelSerializer


class OfferSerializer(ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"
