from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from serial.api_views import SearchSerialFilterView, SeasonViewSet, SerialViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("series", SerialViewSet)
router.register("series/seasons", SeasonViewSet)
router.register("search/series", SearchSerialFilterView)

urlpatterns = router.urls
