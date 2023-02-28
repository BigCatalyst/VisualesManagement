from django_filters import FilterSet, filters
from music.models import Album, Song


class AlbumFilterBackend(FilterSet):
    initial = filters.CharFilter(field_name="title", lookup_expr="istartswith")

    class Meta:
        model = Album
        exclude = [
            "id",
            "title",
            "year",
            "photo",
            "author_navigation_id",
            "author",
            "photo_back",
        ]


class SongFilterBackend(FilterSet):
    initial = filters.CharFilter(
        field_name="title", lookup_expr="istartswith", label="Initial letter."
    )

    class Meta:
        model = Song
        exclude = ["id", "title", "success", "video", "collection"]
