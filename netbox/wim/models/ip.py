
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from netbox.models import PrimaryModel


# __all__ = (
#     'WebIPAddress',
# )


# class WebIPAddress(PrimaryModel):
#     """ 
#     An IP Address, separate from the IPAM version until it gets further built out.
#     """
#     address = models.GenericIPAddressField(
#         _('Address'),
#         protocol='IPv4',
#     )
    
#     class Meta:
#         ordering = ('address', 'pk')
#         verbose_name = 'IP Address'
#         verbose_name_plural = 'IP Addresses'

#     def __str__(self):
#         return str(self.address)
    
#     def get_absolute_url(self):
#         return reverse('wim:webipaddress', args=[self.pk])
