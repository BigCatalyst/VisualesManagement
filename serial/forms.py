from django import forms
from serial.models import Season, Serial


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Serial
        fields = "__all__"


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = "__all__"
