from offer.models import Offer
from offer.serializers import OfferSerializer
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class OfferViewSet(ModelViewSet):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    parser_class = (FileUploadParser, FormParser, MultiPartParser)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(OfferViewSet, self).get_permissions()
