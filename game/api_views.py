from django_filters.rest_framework import DjangoFilterBackend
from game.filters import GameFilterBackend
from game.models import Category, Game
from game.serializers import CategorySerializer, GameSerializer
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet


class GameViewSet(ModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all()
    parser_class = (FileUploadParser, FormParser, MultiPartParser)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(GameViewSet, self).get_permissions()


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    parser_class = (FileUploadParser, FormParser, MultiPartParser)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(CategoryViewSet, self).get_permissions()


class SearchGameFilterView(ListModelMixin, GenericViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = GameFilterBackend
    search_fields = ["name"]
    filterset_fields = ["initial"]
