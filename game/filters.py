from django_filters import FilterSet, filters
from game.models import Game


class GameFilterBackend(FilterSet):
    initial = filters.CharFilter(field_name="name", lookup_expr="istartswith")

    class Meta:
        model = Game
        exclude = [
            "id",
            "name",
            "year",
            "category",
            "photo",
            "manual",
            "synopsis",
            "type",
            "size",
            "requirement",
            "capture",
        ]
