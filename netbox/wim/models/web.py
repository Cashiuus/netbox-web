import datetime

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

from netbox.models import OrganizationalModel, PrimaryModel
from utilities.choices import ColorChoices
from utilities.fields import ColorField, NaturalOrderingField
from wim.choices import *


__all__ = (
    'Certificate',
    'OperatingSystem',
    'ParkedStatus',
    'Software',
    'WebEmail',
)



class Certificate(PrimaryModel):
    """
    An encryption certificate generated to run on and/or provide security support for
    the transport protocol of a web service.

    Using SHA1 hash as the main unique field across other models for FK's.

    Field List:
        hash_sha1, hash_sha256, hash_md5, sdn, scn, san, sorg,
        idn, icn, iorg, date_issued, date_expiration, signing_algorithm,
        key_type, key_bitlength, is_wildcard, is_self_signed,
        date_created, date_modified

    +NetBox Built-In Fields:
        description, comments,

    """
    hash_sha1 = models.CharField(_('SHA1'), max_length=50, unique=True)
    hash_sha256 = models.CharField(_('SHA256'), max_length=65, blank=True)
    hash_md5 = models.CharField(_('MD5'), max_length=32, blank=True)

    sdn = models.CharField(_('Subject DN'), max_length=400)
    scn = models.CharField(_('Subject CN'), max_length=400, blank=True)
    san = models.TextField(_('Subject AN'), blank=True)
    sorg = models.CharField(_('Subject Org'), max_length=400, blank=True)
    idn = models.CharField(_('Issuer DN'), max_length=400)
    icn = models.CharField(_('Issuer CN'), max_length=400, blank=True)
    iorg = models.CharField(_('Issuer Org'), max_length=400, blank=True)
    date_issued = models.DateField(_('Issued Date'), blank=True)
    date_expiration = models.DateField(_('Expiration Date'),
                                        help_text='TLS Cert expiration date')

    # Extra/Optional fields, cannot get these via httpx, but perhaps another way
    # Choices
    signing_algorithm = models.CharField(
        _('Signing Algorithm'),
        max_length=20,
        blank=True,
        choices=CertSigningAlgorithmChoices,
        # default=CertSigningAlgorithmChoices.HASH_SHA256,
        help_text='Signing algorithm hash function',
    )
    key_type = models.CharField(
        _('Key Type'),
        max_length=20,
        blank=True,
        choices=CertKeyTypeChoices,
        # default=CertKeyTypeChoices.TYPE_RSA,
        help_text='The encryption key type',
    )
    key_bitlength = models.CharField(
        _('Key Bit Length'),
        max_length=20,
        blank=True,
        choices=CertBitLengthChoices,
        # default=CertBitLengthChoices.BITLENGTH_2048,
        help_text='The encryption key bith length (commonly 2048)',
    )

    # Reconfigured these two Booleans like other NetBox models, without any
    # null ("Unknown") effect
    # Default None makes these start as "Unknown"
    is_wildcard = models.BooleanField(_('Cert Is Wildcard'), default=False)
    is_self_signed = models.BooleanField(_('Is Self-Signed'), default=False)

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

    class Meta:
        # default_manager_name =
        ordering = ['scn']
        verbose_name = _('Certificate')
        verbose_name_plural = _('Certificates')

    def __str__(self):
        return self.hash_sha1

    def get_absolute_url(self):
        return reverse('wim:certificate', args=[self.pk])

    # Help on these methods: https://docs.djangoproject.com/en/5.0/intro/tutorial02/
    def has_expired_cert(self):
        """
        Usage:  q = Certificate.objects.get(pk=1)
                q.has_expired_cert()
                >>> False | True
        """
        return self.date_expiration < timezone.now()

    def has_expiring_cert(self):
        """
        Usage:  q = Certificate.objects.get(pk=1)
                q.has_expiring_cert()
                >>> False | True
        """
        # Cert expiration is greater than today, but less than 30 days from now
        return self.date_expiration > timezone.now() and self.date_expiration < timezone.now() + datetime.timedelta(days=30)



# class AssetClass(OrganizationalModel):
#     """
#     Primary classficiation types for assets in our inventory
#     (Domain, FQDN, Server, etc).
#     """
#     name = models.CharField(
#         _('Type'),
#         max_length=100,
#         unique=True,
#         help_text='An asset type category'
#     )
#     slug = models.SlugField(max_length=100)
#     # order = models.SmallIntegerField(default=10)
#     # color = models.CharField(max_length=20, default="#FF0000")

#     class Meta:
#         #default_manager_name =
#         ordering = ['name']
#         verbose_name = _('Asset Class')
#         verbose_name_plural = _('Asset Classes')

#     def __str__(self):
#         return self.name


# class FqdnStatus(OrganizationalModel):
#     """ A basic operational status for FQDNs. """
#     name = models.CharField(_('Name'), max_length=50, unique=True)
#     description = models.TextField(_('Description'))
#     order = models.SmallIntegerField(default=10)
#     color = ColorField(
#         default=ColorChoices.COLOR_GREY
#     )
#     # color = models.CharField(max_length=20, default="#FF0000")

#     class Meta:
#         ordering = ('order', 'name')
#         verbose_name = _('FQDN Status')
#         verbose_name_plural = _('FQDN Statuses')

#     def __str__(self):
#         return self.name


# class WebsiteStatus(OrganizationalModel):
#     """ A basic operational status for Live Websites. """
#     name = models.CharField(_('Name'), max_length=50, unique=True)
#     description = models.TextField(_('Description'))
#     order = models.SmallIntegerField(default=10)
#     color = ColorField(
#         default=ColorChoices.COLOR_GREY
#     )
#     # color = models.CharField(max_length=20, default="#FF0000")

#     class Meta:
#         ordering = ('order', 'name')
#         verbose_name = _('Website Status')
#         verbose_name_plural = _('Website Statuses')

#     def __str__(self):
#         return self.name


class ParkedStatus(OrganizationalModel):
    """ A parked (301/302) status for FQDNs, separating if we are handling the park or if its a 3rd party. """
    name = models.CharField(_('Name'), max_length=50, unique=True)
    description = models.TextField(_('Description'))
    order = models.SmallIntegerField(default=10)
    color = ColorField(
        default=ColorChoices.COLOR_GREY
    )
    # color = models.CharField(max_length=20, default="#FF0000")

    class Meta:
        ordering = ('order', 'name')
        verbose_name = _('Parked Status')
        verbose_name_plural = _('Parked Statuses')

    def __str__(self):
        return self.name


class OperatingSystem(OrganizationalModel):
    """
    An operating system definition to be used with Assets.
    """
    # Default orgmodel fields: name, slug, description
    vendor = models.CharField(_('Vendor'), max_length=100)
    product = models.CharField(
        _('Product Name'),
        max_length=100,
        help_text=_('Product name and major version')
    )
    update = models.CharField(
        _('Update/Service Pack'),
        max_length=10,
        blank=True,
        help_text='Revision or Service Pack value'
    )
    platform_family = models.CharField(
        _('Platform Family'),
        max_length=50,
        choices=PlatformFamilyChoices,
        blank=True,
        help_text='The main OS family, such as Linux, Windows, or OSX'
    )
    # NOTE: This could point to DeviceRole table, has things like Database Server, Application Server, etc.
    platform_type = models.CharField(
        _('Platform Type'),
        max_length=50,
        choices=PlatformTypeChoices,
        default=PlatformTypeChoices.PLATFORMTYPE_SERVER,
        help_text='The category type of platform to which this belongs'
    )
    build_number = models.CharField(_("OS Build"), max_length=50, blank=True)
    cpe = models.OneToOneField(
        to='wim.CPE',
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True,
        verbose_name='CPE'
    )
    color = ColorField(
        default=ColorChoices.COLOR_GREY
    )

    class Meta:
        ordering = ['name']
        # ordering = ['vendor', 'product']
        # unique_together = ['vendor', 'product', 'update']
        verbose_name = _('Operating System')
        verbose_name_plural = _('Operating Systems')

    def __str__(self):
        return u'%s %s %s' % (self.vendor, self.product, self.update)

    def get_absolute_url(self):
        return reverse('wim:operatingsystem', args=[self.pk])


class Software(OrganizationalModel):
    """
    Software, technologies, or webserver frameworks as products and versions assigned
    to an asset observed with the respective product and version.
    """
    name = models.CharField(
        _('Name'),
        max_length=50,
        unique=True,
        help_text='The name and version of the server framework (e.g. Apache/2.4.9)'
    )
    product = models.CharField(_('product'), max_length=250, blank=True, default='')
    version = models.CharField(_('version'), max_length=50, blank=True, default='')
    cpe = models.ForeignKey(
        to='wim.CPE',
        on_delete=models.PROTECT,
        related_name='software',
        blank=True, null=True,
        verbose_name='CPE',
    )
    raw_banner = models.CharField(_('Raw Banner'), max_length=300, blank=True)
    order = models.SmallIntegerField(default=10)
    # color = models.CharField(max_length=20, default="#FF0000")
    notes = models.TextField(_('Notes'), blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Software')
        verbose_name_plural = _('Software')

    def __str__(self):
        return self.name
        #return '{0}/{1}'.format(self.product, self.version)

    def get_absolute_url(self):
        return reverse('wim:software', args=[self.pk])


class WebEmail(OrganizationalModel):
    """
    A short-term solution for cross-referencing/grouping email addresses
    found during web/dns recon, rather than simply using a Char/EmailField in tables.

    This will be used as a ManyToMany field in the main datasets.
    """

    # TODO: Extract the root domain of the email address and
    # link it to a domain root, always or only if the domain already exists,
    # meaning it's a domain that we know about and are tracking/inventorying?!?

    email_address = models.EmailField(
        unique=True,
    )
    # domain = models.CharField(_('Domain'), max_length=150)
    domain = models.ForeignKey(
        'Domain',
        on_delete=models.PROTECT,
        related_name='emails',
        blank=True,
        null=True,
        help_text=_('Web domain of the email address for this contact'),
    )

    class Meta:
        ordering = ('email_address',)

    def __str__(self):
        return self.email_address

    def get_absolute_url(self):
        return reverse('wim:webemail', args=[self.pk])

    # def get_domain(self):
    #     s = f"{self.email_address}"
    #     return s.split("@")[1]

    def save(self, *args, **kwargs):
        """
        Override default save so we can derive domain from
        the input email address automatically.
        """
        # Either get the string needed here or do it via callable
        # self.domain = self.get_domain()
        s = f"{self.email_address}"
        self.domain = s.split("@")[1]
        super().save(*args, **kwargs)
