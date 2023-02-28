from django.conf import settings
from django.urls import include
from django.urls.conf import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from cinema.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path("", include("game.urls"), name="games"),
    path("", include("movie.urls"), name="movies"),
    path("", include("music.urls"), name="music"),
    path("", include("offer.urls"), name="offers"),
    path("", include("serial.urls"), name="series"),
]
