from django.conf import settings
from game.api_views import CategoryViewSet, GameViewSet, SearchGameFilterView
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("games", GameViewSet)
router.register("game/categories", CategoryViewSet)
router.register("search/games", SearchGameFilterView, basename="search_games")

urlpatterns = router.urls
