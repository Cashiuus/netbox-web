from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from netbox.models import OrganizationalModel

__all__ = (
    'Brand',
)


class Brand(OrganizationalModel):
    """
    A Brand is a major brand, segment, acquisition, or recognizable component
    of the company to which it's important to attribute assets.
    """
    # OrganizationalModel class automatically comes with: name, slug, description

    # notes = models.TextField(_('Notes'), blank=True, default='',
    #                          help_text='Notable remarks about this division, such as brand names associated')
    date_created = models.DateTimeField(_('Date Created'), auto_now_add=True,
                                        help_text='system field for creation date')
    date_modified = models.DateTimeField(_('Date Modified'), auto_now=True,
                                         help_text='system field for modified date')

    class Meta:
        ordering = ['name']
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wim:brand', args=[self.pk])