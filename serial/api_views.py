from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from serial.filters import SerialFilterBackend
from serial.models import Season, Serial
from serial.serializers import SeasonSerializer, SerialSerializer


class SerialViewSet(ModelViewSet):
    serializer_class = SerialSerializer
    queryset = Serial.objects.all()
    parser_class = (FileUploadParser, FormParser, MultiPartParser)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(SerialViewSet, self).get_permissions()


class SeasonViewSet(ModelViewSet):
    serializer_class = SeasonSerializer
    queryset = Season.objects.all()

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(SeasonViewSet, self).get_permissions()


class SearchSerialFilterView(ListModelMixin, GenericViewSet):
    serializer_class = SerialSerializer
    queryset = Serial.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = SerialFilterBackend
    search_fields = ["title_eng"]
    filterset_fields = ["initial"]
