from django.urls.conf import path
from django.views.decorators.cache import cache_page
from music import views

urlpatterns = [
    path("music/", views.music_page, name="site_music_page"),
    path(
        "music/collection/<int:pk>/details/",
        cache_page(60 * 1440)(views.CollectionDetail.as_view()),
        name="site_collection_detail",
    ),
    path(
        "music/concert/<int:pk>/details/",
        cache_page(60 * 1440)(views.ConcertDetail.as_view()),
        name="site_concert_detail",
    ),
    path(
        "music/dvd/<int:pk>/details/", cache_page(60 * 1440)(views.DVDDetail.as_view()), name="site_dvd_detail"
    ),
    path(
        "music/album/<int:pk>/details/",
        cache_page(60 * 1440)(views.AlbumDetail.as_view()),
        name="site_album_detail",
    ),
    path(
        "music/author/<int:pk>/details/",
        cache_page(60 * 1440)(views.AuthorDetail.as_view()),
        name="site_author_detail",
    ),
    path("music/gender/", views.music_gender_page, name="site_music_genders_page"),
]
