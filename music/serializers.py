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
from rest_framework.serializers import ModelSerializer


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class AlbumSerializer(ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"


class ConcertSerializer(ModelSerializer):
    class Meta:
        model = Concert
        fields = "__all__"


class AlbumSongSerializer(ModelSerializer):
    class Meta:
        model = AlbumSong
        fields = "__all__"


class DVDSerializer(ModelSerializer):
    class Meta:
        model = DVD
        fields = "__all__"


class DVDSongSerializer(ModelSerializer):
    class Meta:
        model = DVDSong
        fields = "__all__"


class CollectionSerializer(ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"


class SongSerializer(ModelSerializer):
    class Meta:
        model = Song
        fields = "__all__"
