from django_filters import FilterSet, filters
from serial.models import Serial


class SerialFilterBackend(FilterSet):
    initial = filters.CharFilter(field_name="title_eng", lookup_expr="istartswith")

    class Meta:
        model = Serial
        fields = ["type", "gender__name", "origen"]
        exclude = [
            "id",
            "title",
            "title_eng",
            "gender",
            "synopsis",
            "photo",
            "initial",
            "in_transmission",
            "actor",
        ]
