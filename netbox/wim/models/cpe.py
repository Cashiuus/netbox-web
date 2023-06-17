
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _





class CPE(models.Model):
    """
    A Common Platform Enumeration (CPE) object string for use with automation.
    """
    cpe = models.CharField(
        _('CPE'),
        max_length=300, unique=True,
        help_text='The machine readable CPE string'
    )
    cpe_friendly = models.CharField(
        _('CPE Friendly'),
        max_length=300,
        blank=True,
        null=True,
        help_text='Human readable CPE string description'
    )
    # description = models.TextField(blank=True)

    class Meta:
        ordering = ('cpe',)
    
    def __str__(self):
        self.cpe
    
    def get_absolute_url(self):
        return reverse('wim:cpe', args=[self.pk])
