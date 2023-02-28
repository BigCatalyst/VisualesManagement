from django_filters import FilterSet, filters
from movie.models import Movie


class MovieFilterBackend(FilterSet):
    initial = filters.CharFilter(field_name="title_eng", lookup_expr="istartswith")

    class Meta:
        model = Movie
        fields = ["gender__name", "actor__name", "saga__title", "origen"]
        exclude = [
            "id",
            "title_eng",
            "title",
            "sub_gender",
            "duration",
            "year",
            "format",
            "synopsis",
            "initial",
            "photo",
            "definition",
            "language",
        ]
