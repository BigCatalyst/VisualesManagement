from actor.models import Actor
from django_filters.rest_framework import DjangoFilterBackend
from movie.filters import MovieFilterBackend
from movie.models import (
    Combo,
    ComboMovie,
    Documental,
    DocumentalSeason,
    Format,
    Gender,
    GenderDocumental,
    Humor,
    Movie,
    Sagas,
    Sport,
)
from movie.serializers import (
    ActorSerializer,
    ComboMovieSerializer,
    ComboSerializer,
    DocumentalSeasonSerializer,
    DocumentalSerializer,
    FormatSerializer,
    GenderDocumentalSerializer,
    GenderSerializer,
    HumorSerializer,
    MovieSerializer,
    SagasSerializer,
    SportSerializer,
)
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet


class ActorViewSet(ModelViewSet):
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()
    parser_class = (FileUploadParser, FormParser, MultiPartParser)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(ActorViewSet, self).get_permissions()


class MovieViewSet(ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    parser_class = (FileUploadParser, FormParser, MultiPartParser)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(MovieViewSet, self).get_permissions()


class SportViewSet(ModelViewSet):
    serializer_class = SportSerializer
    queryset = Sport.objects.all()
    parser_class = (FileUploadParser, FormParser, MultiPartParser)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(SportViewSet, self).get_permissions()


class DocumentalViewSet(ModelViewSet):
    serializer_class = DocumentalSerializer
    queryset = Documental.objects.all()
    parser_class = (FileUploadParser, FormParser, MultiPartParser)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(DocumentalViewSet, self).get_permissions()


class DocumentalSeasonViewSet(ModelViewSet):
    serializer_class = DocumentalSeasonSerializer
    queryset = DocumentalSeason.objects.all()

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(DocumentalSeasonViewSet, self).get_permissions()


class FormatViewSet(ModelViewSet):
    serializer_class = FormatSerializer
    queryset = Format.objects.all()

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(FormatViewSet, self).get_permissions()


class GenderDocumentalViewSet(ModelViewSet):
    serializer_class = GenderDocumentalSerializer
    queryset = GenderDocumental.objects.all()
    parser_class = (FileUploadParser, FormParser, MultiPartParser)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(GenderDocumentalViewSet, self).get_permissions()


class GenderViewSet(ModelViewSet):
    serializer_class = GenderSerializer
    queryset = Gender.objects.all()
    parser_class = (FileUploadParser, FormParser, MultiPartParser)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(GenderViewSet, self).get_permissions()


class HumorViewSet(ModelViewSet):
    serializer_class = HumorSerializer
    queryset = Humor.objects.all()
    parser_class = (FileUploadParser, FormParser, MultiPartParser)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(HumorViewSet, self).get_permissions()


class ComboViewSet(ModelViewSet):
    serializer_class = ComboSerializer
    queryset = Combo.objects.all()
    parser_class = (FileUploadParser, FormParser, MultiPartParser)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(ComboViewSet, self).get_permissions()


class ComboMovieViewSet(ModelViewSet):
    serializer_class = ComboMovieSerializer
    queryset = ComboMovie.objects.all()

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(ComboMovieViewSet, self).get_permissions()


class SagasViewSet(ModelViewSet):
    serializer_class = SagasSerializer
    queryset = Sagas.objects.all()

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(SagasViewSet, self).get_permissions()


class SearchMovieFilterView(ListModelMixin, GenericViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = MovieFilterBackend
    search_fields = ["title_eng"]
    filterset_fields = ["initial"]
