from actor.models import Actor
from django import forms
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


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = "__all__"


class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = "__all__"


class SportForm(forms.ModelForm):
    class Meta:
        model = Sport
        fields = "__all__"


class DocumentalForm(forms.ModelForm):
    class Meta:
        model = Documental
        fields = "__all__"


class DocumentalSeasonForm(forms.ModelForm):
    class Meta:
        model = DocumentalSeason
        fields = "__all__"


class FormatForm(forms.ModelForm):
    class Meta:
        model = Format
        fields = "__all__"


class GenderDocumentalForm(forms.ModelForm):
    class Meta:
        model = GenderDocumental
        fields = "__all__"


class GenderForm(forms.ModelForm):
    class Meta:
        model = Gender
        fields = "__all__"


class HumorForm(forms.ModelForm):
    class Meta:
        model = Humor
        fields = "__all__"


class ComboForm(forms.ModelForm):
    class Meta:
        model = Combo
        fields = "__all__"


class ComboMovieForm(forms.ModelForm):
    class Meta:
        model = ComboMovie
        fields = "__all__"


class SagasForm(forms.ModelForm):
    class Meta:
        model = Sagas
        fields = "__all__"
