
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from netbox.models import OrganizationalModel


__all__ = (
    # 'Registrar',
    'Vendor',
)


class Vendor(OrganizationalModel):
    """
    A vendor is a hosting, web design or similar type company contracted to provide
    infrastructure or services that directly support a web property.
    TODO: I wonder if this can be lifted over to "Provider" in the circuits app.
    """
    # This is built based on how Netbox did: dcim:manufacturer
    contacts = GenericRelation(
        to='tenancy.ContactAssignment'
    )

    def get_absolute_url(self):
        return reverse('wim:vendor', args=[self.pk])




# class Registrar(OrganizationalModel):
#     """
#     A registrar is a company which provides domain registration services
#     and will be used for the Domains dataset.
#     """
#     # This is built based on how Netbox did: dcim:manufacturer
#     contacts = GenericRelation(
#         to='tenancy.ContactAssignment'
#     )

#     iana_id = models.IntegerField(_('Registrar IANA ID'), blank=True, null=True)

#     def get_absolute_url(self):
#         return reverse('wim:registrar', args=[self.pk])
