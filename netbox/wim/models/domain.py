import datetime

import netaddr
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


# from netbox.config import get_config
from netbox.models import PrimaryModel
from wim.validators import DNSValidator
from wim.choices import *
# This has to be imported this way to avoid circular import error
# for FQDN referenced in function below
from wim.models import FQDN


__all__ = (
    'Domain',
)


class Domain(PrimaryModel):
    """
    A root/parent web domain which will house WHOIS registrar details
    and be tied to FQDN's/Subdomains.
    """
    name = models.CharField(
        _('Name'),
        max_length=255,
        unique=True,
        validators=[DNSValidator],
        help_text='A top-level/parent web domain'
    )

    # status_orig = models.IntegerField(
    #     _('Status_orig'),
    #     choices=RECORD_STATUS_CHOICES,
    #     default=RECORD_STATUS_CHOICES.new,
    #     help_text='Operational status of this Domain'
    # )

    status = models.CharField(
        _('Status'),
        max_length=50,
        choices=DomainStatusChoices,
        default=DomainStatusChoices.STATUS_NEW,
        help_text='Operational status of this Domain',
    )

    slug = models.SlugField(max_length=100)

    asset_confidence = models.CharField(
        _('Confidence'),
        max_length=50,
        choices=AssetConfidenceChoices,
        default=AssetConfidenceChoices.CONFIDENCE_CANDIDATE,
        help_text='Asset attribution confidence level',
    )

    brand = models.ForeignKey(
        'Brand',
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='domains',
        help_text=_('Brand'),
    )

    ownership_type = models.CharField(
        _('Ownership Type'),
        max_length=100,
        choices=DomainOwnershipStatusChoices,
        default=DomainOwnershipStatusChoices.OWNEDSTATUS_UNKNOWN,
        help_text="Primary ownership of this domain (e.g. who owns it)",
    )

    # prev name: registrar_expiry_date
    date_registrar_expiry = models.DateField(
        _('Domain Expiration'),
        blank=True, null=True,
    )
    # prev name: date_first_seen
    date_first_registered = models.DateField(
        _('Date Registered'),
        blank=True, null=True,
    )
    date_last_recon_scanned = models.DateField(
        _('Date Last Scanned'),
        blank=True, null=True,
        help_text='Date this domain was last scanned by web recon workflow'
    )
    # linked_company = models.ForeignKey('Company', on_delete=models.CASCADE,
    #                                    blank=True, null=True,
    #                                    verbose_name='Linked Company')
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.CASCADE,
        related_name='domains',
        blank=True,
        null=True
    )

    # prev name: internet_facing
    is_internet_facing = models.BooleanField(
        _('Internet Facing'),
        null=True, default=True,
        help_text='Most domains are internet-facing unless used for internal network only',
    )
    # prev name: flagship
    is_flagship = models.BooleanField(_('Flagship'), null=True, default=False)

    # TODO: Other netbox models don't usee "null=True" in here, maybe this is causing issues
    # prev name: reg_matches_standards
    meets_standards = models.BooleanField(
        _('Meets Standards'),
        null=True, default=True,
        help_text='Domain registration meets company technical standards',
    )

    # internal_ad_domain = models.BooleanField(_('AD Domain'), null=True, default=False)
    registrar_iana_id_orig = models.IntegerField(_('Registrar IANA ID (orig)'), blank=True, null=True)
    registrar_company_orig = models.CharField(
        _('Registrar Name (orig)'),
        max_length=255,
        blank=True,
    )
    # TODO: If i do a Registrar table, it could be done just like the RIR table
    # registrar_company = models.ForeignKey(
    #     to='wim.Registrar',
    #     on_delete=models.PROTECT,
    #     related_name='domains',
    #     blank=True,
    #     null=True,
    #     verbose_name='Registrar',
    # )

    registrant_org = models.CharField(
        _('Registrant Org'),
        max_length=255,
        blank=True
    )
    # registrant_email = models.CharField(_('Registrant Email'), max_length=255, blank=True, default='')
    registration_emails_orig = models.TextField(
        _('Email Addresses (orig)'),
        blank=True,
        help_text='List of email addresses tied to a whois registration for this domain',
    )
    registration_emails = models.ManyToManyField(
        to='wim.WebEmail',
        related_name='domains',
        blank=True,
        verbose_name='Registration Emails',
    )
    registrar_domain_statuses = models.TextField(
        _('Domain Statuses'),
        blank=True, default='',
        help_text='Domain statuses, such as ClientTransferProhibited',
    )
    nameservers = models.TextField(
        _('Nameservers'),
        blank=True,
        help_text='Comma-separated list of authoritative namservers for this domain',
    )
    mail_servers = models.CharField(_('Mail Servers'), max_length=255, blank=True, default='')
    whois_servers = models.CharField(_('Whois Servers'), max_length=255, blank=True, default='')
    soa_nameservers = models.CharField(_('SOA Nameservers'), max_length=255, blank=True, default='')
    soa_email = models.EmailField(_('SOA Email'), max_length=255, blank=True, default='')
    #alexa_ranked = models.BooleanField(_('Alexa Ranked'), null=True, default=False)

    date_created = models.DateTimeField(
        _('Date Created'),
        auto_now_add=True,
        help_text='system field for creation date',
    )
    date_modified = models.DateTimeField(
        _('Date Modified'),
        auto_now=True,
        help_text='system field for modified date',
    )

    notes = models.TextField(_('Notes'), blank=True, default='')

    # @property
    # def count_fqdns():
    #     """ Get a count of assets for this domain. """
    #     # Reference: djangoproject.com - aggregation
    #     return FQDN.objects.filter(domain=self.name).count()

    class Meta:
        # default_manager_name =
        ordering = ['name']
        verbose_name = _('Domain')
        verbose_name_plural = _('Domains')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wim:domain', args=[self.pk])

    def get_child_fqdns(self):
        """
        Return all FQDNs that are children of this root domain.
        """
        return FQDN.objects.filter(
            domain=self.name,
        )

    def get_status_color(self):
        return DomainStatusChoices.colors.get(self.status)

    def get_ownership_type_color(self):
        return DomainOwnershipStatusChoices.colors.get(self.ownership_type)
