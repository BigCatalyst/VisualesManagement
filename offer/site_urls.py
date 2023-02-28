from django.urls.conf import path

from . import views

urlpatterns = [
    path("offers/", views.offers_page, name="site_offers_page"),
    path("estrenos/", views.latest_media_page, name="site_latest_media_page"),
    path("offers/type/", views.offers_type_page, name="site_offers_type_page"),
    path("offers/list/", views.OfferList.as_view(), name="site_offers_list"),
    path(
        "offers/detail/<int:pk>/",
        views.OfferDetail.as_view(),
        name="site_offers_details",
    ),
]
