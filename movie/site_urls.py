from django.urls.conf import path
from movie import views
from django.views.decorators.cache import cache_page


urlpatterns = [
    path("movies/", views.movies_page, name="site_movies_page"),
    path(
        "movies/sagas/<int:pk>/", cache_page(60 * 1440)(views.SagaDetail.as_view()), name="site_sagas_detail"
    ),
    path(
        "movies/combos/<int:pk>/", cache_page(60 * 1440)(views.ComboDetail.as_view()), name="site_combo_detail"
    ),
    path(
        "movies/detail/<int:pk>/",
        cache_page(60 * 1440)(views.MovieDetail.as_view()),
        name="site_movies_detail",
    ),
    path(
        "movies/actors/detail/<int:pk>/",
        cache_page(60 * 1440)(views.ActorDetail.as_view()),
        name="site_actors_detail",
    ),
    path("movies/gender/", views.movies_gender_page, name="site_movies_gender_page"),
    path("movies/actors/", views.movies_actors_page, name="site_movies_actors_page"),
    path("sports/", views.sports_page, name="site_sports_page"),
    path(
        "sports/details/<int:pk>/",
        cache_page(60 * 1440)(views.SportDetails.as_view()),
        name="site_sports_details",
    ),
    path("animados/", views.animados_page, name="site_animados_page"),
    path("cinemateca/", views.cinemateca_page, name="site_cinemateca_page"),
    path(
        "cinemateca/humor/<int:pk>/details/",
        cache_page(60 * 1440)(views.HumorDetail.as_view()),
        name="site_humor_detail",
    ),
    path("documentales/", views.documental_page, name="site_documental_page"),
    path(
        "documentales/details/<int:pk>/",
        cache_page(60 * 1440)(views.DocumentalDetail.as_view()),
        name="site_documental_details",
    ),
    path(
        "documentales/gender/",
        views.documental_gender_page,
        name="site_documental_gender_page",
    ),
    path(
        "admins/videos/list/",
        views.admin_video_list_page,
        name="site_admin_video_list_page",
    ),
    path(
        "admins/audios/list/",
        views.admin_audio_list_page,
        name="site_admin_audio_list_page",
    ),
]
