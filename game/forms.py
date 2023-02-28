from django import forms
from game.models import Category, Game


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = "__all__"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
