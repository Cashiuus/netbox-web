
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
    # NOTE: Remember, the org model parent class comes w/ default ields already
    #   - name, description, slug, objects

    url = models.URLField(_('Vendor URL'), blank=True, null=True)
    # This is built based on how Netbox did: dcim:manufacturer
    contacts = GenericRelation(
        to='tenancy.ContactAssignment'
    )

    vendor_pocs_orig = models.CharField(
        _('Vendor POCs'), 
        max_length=500, 
        blank=True, 
        help_text='One or more vendor POCs that support this web property'
    )
    notes = models.TextField(_('Vendor Notes'), blank=True, default='')
    
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
