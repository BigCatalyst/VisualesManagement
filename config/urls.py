from django.conf import settings
#from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from movie.views import HomeView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from tasks.views import (
    load_data_view,
    load_data1_view,
    load_data2_view,
    load_data3_view,
)

from config.settings.base import env

from django.urls import re_path

urlpatterns = [
    path('summernote/', include('django_summernote.urls')),
    path("", HomeView.as_view(), name="home"),
    path("load-data/", load_data_view, name="load-data"),
    path("load-data-1/", load_data1_view, name="load-data-1"),
    path("load-data-2/", load_data2_view, name="load-data-2"),
    path("load-data-3/", load_data3_view, name="load-data-3"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("cinema.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    re_path('^searchableselect/', include('searchableselect.urls')),
    path("", include("movie.site_urls")),
    path("", include("offer.site_urls")),
    path("", include("music.site_urls")),
    path("", include("game.site_urls")),
    path("", include("serial.site_urls")),
    path("", include(("tasks.urls", "tasks"), namespace="tasks"))
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

schema_view = get_schema_view(
    openapi.Info(
        title="Cinema API",
        default_version=env("HEROKU_RELEASE_VERSION", default="v1"),
        description="Cinema API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="info@byt.bz"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
