
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from netbox.models import PrimaryModel


__all__ = (
    'WebEmail',
)


class WebEmail(PrimaryModel):
    """
    A short-term solution for cross-referencing/grouping email addresses
    found during web/dns recon, rather than simply using a Char/EmailField in tables.
    """

    # TODO: Extract the root domain of the email address and 
    # link it to a domain root, always or only if the domain already exists,
    # meaning it's a domain that we know about and are tracking/inventorying?!?
    
    email_address = models.EmailField(
        unique=True,
        blank=True
    )
    domain_tmp = models.CharField(_('Domain_tmp'), max_length=150)

    class Meta:
        ordering = ('email_address',)

    def __str__(self):
        self.email_address
    
    def get_absolute_url(self):
        return reverse('wim:webemail', args=[self.pk])
