from django.urls.conf import path

from tasks.views import LicenseView

urlpatterns = [
    path("license/", LicenseView.as_view(), name="license"),
]
