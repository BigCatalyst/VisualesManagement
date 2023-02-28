from django.conf import settings
from music.api_views import *  # noqa
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("songs", SongViewSet)  # noqa F405
router.register("songs/collection", CollectionViewSet)  # noqa F405
router.register("songs/authors", AuthorViewSet)  # noqa F405
router.register("dvd", DVDViewSet)  # noqa F405
router.register("dvd/songs", DVDSongViewSet)  # noqa F405
router.register("albums/songs", AlbumSongViewSet)  # noqa F405
router.register("albums", AlbumViewSet)  # noqa F405
router.register("concerts", ConcertViewSet)  # noqa F405
router.register("search/albums", SearchAlbumFilterView)  # noqa F405
router.register("search/songs", SearchSongFilterView)  # noqa F405


urlpatterns = router.urls
