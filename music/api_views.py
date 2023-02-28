from django_filters.rest_framework import DjangoFilterBackend
from music.filters import AlbumFilterBackend, SongFilterBackend
from music.models import (
    DVD,
    Album,
    AlbumSong,
    Author,
    Collection,
    Concert,
    DVDSong,
    Song,
)
from music.serializers import (
    AlbumSerializer,
    AlbumSongSerializer,
    AuthorSerializer,
    CollectionSerializer,
    ConcertSerializer,
    DVDSerializer,
    DVDSongSerializer,
    SongSerializer,
)
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet


class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    parser_class = (FileUploadParser, FormParser, MultiPartParser)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(AuthorViewSet, self).get_permissions()


class AlbumViewSet(ModelViewSet):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()
    parser_class = (FileUploadParser, FormParser, MultiPartParser)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(AlbumViewSet, self).get_permissions()


class ConcertViewSet(ModelViewSet):
    serializer_class = ConcertSerializer
    queryset = Concert.objects.all()
    parser_class = (FileUploadParser, FormParser, MultiPartParser)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(ConcertViewSet, self).get_permissions()


class AlbumSongViewSet(ModelViewSet):
    serializer_class = AlbumSongSerializer
    queryset = AlbumSong.objects.all()

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(AlbumSongViewSet, self).get_permissions()


class DVDViewSet(ModelViewSet):
    serializer_class = DVDSerializer
    queryset = DVD.objects.all()
    parser_class = (FileUploadParser, FormParser, MultiPartParser)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(DVDViewSet, self).get_permissions()


class DVDSongViewSet(ModelViewSet):
    serializer_class = DVDSongSerializer
    queryset = DVDSong.objects.all()

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(DVDSongViewSet, self).get_permissions()


class CollectionViewSet(ModelViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()
    parser_class = (FileUploadParser, FormParser, MultiPartParser)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(CollectionViewSet, self).get_permissions()


class SongViewSet(ModelViewSet):
    serializer_class = SongSerializer
    queryset = Song.objects.all()

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(SongViewSet, self).get_permissions()


class SearchAlbumFilterView(ListModelMixin, GenericViewSet):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = AlbumFilterBackend
    search_fields = ["title"]
    filterset_fields = ["initial"]


class SearchSongFilterView(ListModelMixin, GenericViewSet):
    serializer_class = SongSerializer
    queryset = Song.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = SongFilterBackend
    search_fields = ["title"]
    filterset_fields = ["initial"]
