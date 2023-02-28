from django.urls.conf import path
from serial import views
from django.views.decorators.cache import cache_page


urlpatterns = [
    path("series/", views.series_page, name="site_series_page"),
    path(
        "series/details/<int:pk>/",
        cache_page(60 * 1440)(views.SerialDetail.as_view()),
        name="site_series_details_page",
    ),
    path(
        "series/actors/detail/<int:pk>/",
        cache_page(60 * 1440)(views.ActorDetail.as_view()),
        name="site_actors_series_detail",
    ),
    path("novelas/", views.novela_page, name="site_nov_page"),
]
