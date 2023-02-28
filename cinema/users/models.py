from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from cinema.users.core_model import CoreModel


class User(CoreModel, AbstractUser):
    """Default user for cinema."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    fillables = [
        "is_superuser",
        "is_staff",
        "is_active",
        "username",
        "name",
        "email",
        "password",
    ]
