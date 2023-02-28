from django.urls.conf import path
from game import views
from django.views.decorators.cache import cache_page


urlpatterns = [
    path("games/", views.games_page, name="site_games_page"),
    path(
        "games/<int:pk>/details/", cache_page(60 * 1440)(views.GameDetail.as_view()), name="site_games_details"
    ),
]
