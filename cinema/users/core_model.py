"""This module contain parent class for all service class"""

from django.conf import settings
from django.db import models
from django.db.models import Model
from django.utils.translation import gettext_lazy as _
from rest_framework.utils import model_meta


class CoreModel(Model):
    """Parent class for all Models class"""

    created_at = models.DateTimeField(
        _("Date created"), auto_now_add=True, editable=False
    )
    updated_at = models.DateTimeField(_("Date updated"), auto_now=True, editable=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        db_index=True,
        editable=False,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created",
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        db_index=True,
        editable=False,
        on_delete=models.SET_NULL,
        related_name="%(class)s_modified",
    )

    fillables = ["created_by", "updated_at", "modified_by", "created_at"]

    class Meta:
        """CoreModel class Meta"""

        abstract = True

    @property
    def is_new_instance(self):
        """
        Return if a current instance exist in database
        :return: bool
        """
        return self.id is None

    def get_fillables(self) -> []:
        """
        Return fillable fields
        :return: []
        """
        return self.fillables

    def get_fillable_data(self) -> {}:
        """
        Return a dict with all values with keys included in fillables
        :return: {}
        """
        result = {}
        for field in self.get_fillables():
            try:
                result[field] = getattr(self, field)
            except AttributeError:
                continue

        return result

    def fill(self, attributes: {}) -> None:
        """
        Set specified values on current instance
        :param attributes: Dict
        :return: None
        """
        for attr_name in attributes:
            fillables = self.get_fillables()
            if not fillables:
                raise NotImplementedError(
                    "There is not specified any field as fillable."
                )

            if attr_name in fillables:
                value = attributes[attr_name]
                setattr(self, attr_name, value)

    @property
    def fields_with_relations(self) -> []:
        """
        Return a tuple with list of fields with any relation (many-to-many or
        one-to-many)
        :return: Tuple
        """

        info = model_meta.get_field_info(self)
        many_to_many = []
        one_to_many = []

        for field_name, relation_info in info.relations.items():
            if relation_info.to_many:
                if relation_info.reverse:
                    one_to_many.append(field_name)
                else:
                    many_to_many.append(field_name)

        return many_to_many, one_to_many
