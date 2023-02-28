from actor.models import Actor
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
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class ActorSerializer(ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"


class MovieSerializer(ModelSerializer):
    photo = serializers.ImageField()

    class Meta:
        model = Movie
        fields = "__all__"


class SportSerializer(ModelSerializer):
    class Meta:
        model = Sport
        fields = "__all__"


class DocumentalSerializer(ModelSerializer):
    class Meta:
        model = Documental
        fields = "__all__"


class DocumentalSeasonSerializer(ModelSerializer):
    class Meta:
        model = DocumentalSeason
        fields = "__all__"


class FormatSerializer(ModelSerializer):
    class Meta:
        model = Format
        fields = "__all__"


class GenderDocumentalSerializer(ModelSerializer):
    class Meta:
        model = GenderDocumental
        fields = "__all__"


class GenderSerializer(ModelSerializer):
    class Meta:
        model = Gender
        fields = "__all__"


class HumorSerializer(ModelSerializer):
    class Meta:
        model = Humor
        fields = "__all__"


class ComboSerializer(ModelSerializer):
    class Meta:
        model = Combo
        fields = "__all__"


class ComboMovieSerializer(ModelSerializer):
    class Meta:
        model = ComboMovie
        fields = "__all__"


class SagasSerializer(ModelSerializer):
    class Meta:
        model = Sagas
        fields = "__all__"
