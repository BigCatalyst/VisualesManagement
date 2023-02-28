from django import forms
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


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = "__all__"


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = "__all__"


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = "__all__"


class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = "__all__"


class AlbumSongForm(forms.ModelForm):
    class Meta:
        model = AlbumSong
        fields = "__all__"


class DVDForm(forms.ModelForm):
    class Meta:
        model = DVD
        fields = "__all__"


class DVDSongForm(forms.ModelForm):
    class Meta:
        model = DVDSong
        fields = "__all__"


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = "__all__"
