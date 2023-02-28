from django.conf import settings
from django.urls.conf import path
from movie import views
from movie.api_views import *  # noqa
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("actors", ActorViewSet)  # noqa F405
router.register("movies", MovieViewSet)  # noqa F405
router.register("combo", ComboViewSet)  # noqa F405
router.register("combo/movie", ComboMovieViewSet)  # noqa F405
router.register("sports", SportViewSet)  # noqa F405
router.register("sagas", SagasViewSet)  # noqa F405
router.register("documental", DocumentalViewSet)  # noqa F405
router.register("documental/season", DocumentalSeasonViewSet)  # noqa F405
router.register("gender", GenderViewSet)  # noqa F405
router.register("gender/documental", GenderDocumentalViewSet)  # noqa F405
router.register("format", FormatViewSet)  # noqa F405
router.register("humor", HumorViewSet)  # noqa F405
router.register("search/movies", SearchMovieFilterView)  # noqa F405

urlpatterns = router.urls

site_urls = [
    path("movies", views.movies_page, name="movies"),
]
