from django.conf import settings
from offer.api_views import OfferViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("offers", OfferViewSet)

urlpatterns = router.urls
