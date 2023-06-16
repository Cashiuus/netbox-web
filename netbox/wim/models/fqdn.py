import datetime

import netaddr
from django.contrib.contenttypes.fields import GenericRelation
# from django.contrib.contenttypes.models import ContentType
# from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from netbox.config import get_config
from netbox.models import OrganizationalModel, PrimaryModel
from wim.validators import DNSValidator
from wim.choices import *


__all__ = (
    'FQDN',
)


class FQDN(PrimaryModel):
    """
    A fully-qualified domain name (FQDN/subdomain) representing a web property with some form of
    varying level of active status or usage.
    """
    name = models.CharField(
        _('FQDN'), 
        max_length=255, 
        unique=True,
        validators=[DNSValidator],
        help_text='A fqdn or subdomain of a domain root'
    )
    # TODO: How to best handle slug fields throughout the app
    slug = models.SlugField(max_length=100)

    # My old version of status field
    # status_orig = models.IntegerField(_('Status orig'),
    #                              choices=RECORD_STATUS_CHOICES,
    #                              default=RECORD_STATUS_CHOICES.new,
    #                              help_text='Operational status of this FQDN')

    status = models.CharField(
        _('Status'),
        max_length=50,
        choices=FQDNStatusChoices,
        default=FQDNStatusChoices.STATUS_NEW,
        help_text='Overall operational status of this FQDN'
    )
    status_reason = models.CharField(
        _('Status Reason'),
        max_length=50,
        choices=AssetStatusReasonChoices,
        blank=True,
        help_text='The reason for the current asset status, if applicable'
    )
    # TODO: Refactor...this could be a "tag" or in a separate ticketing type app entirely
    mark_triaging = models.BooleanField(
        _('Triaging'),
        default=False,
        help_text='Currently triaging this asset for investigation or action',
    )
    asset_confidence = models.CharField(
        _('Asset Confidence'),
        max_length=50,
        choices=AssetConfidenceChoices,
        default=AssetConfidenceChoices.CONFIDENCE_CANDIDATE,
        help_text='Asset attribution confidence determination'
    )

    # fqdn_status_orig = models.ForeignKey(
    #     'FqdnStatus',
    #     on_delete=models.CASCADE,
    #     blank=True, null=True,
    #     related_name='fqdns',
    #     verbose_name='FQDN Status'
    # )

    fqdn_status = models.CharField(
        max_length=50,
        choices=FQDNOpsStatusChoices,
        default=FQDNOpsStatusChoices.FQDNSTATUS_UNKNOWN,
        help_text='Technical operational status of this FQDN',
    )

    # website_status_orig = models.ForeignKey(
    #     'WebsiteStatus',
    #     on_delete=models.CASCADE,
    #     blank=True, null=True,
    #     related_name='fqdns',
    #     verbose_name='Website Status'
    # )

    website_status = models.CharField(
        max_length=50,
        choices=WebsiteOpsStatusChoices,
        default=WebsiteOpsStatusChoices.WEBSITESTATUS_UNKNOWN,
        help_text='Technical operational status of this website, if applicable',
    )

    domain = models.ForeignKey(
        'Domain', 
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='fqdns',
        help_text='Root Domain for this entry'
    )

    asset_class = models.CharField(
        max_length=50,
        choices=AssetClassChoices,
        default=AssetClassChoices.ASSET_FQDN,
        help_text=_('Class of web property asset (e.g. Domain or FQDN)')
    )

    website_role = models.CharField(
        max_length=50,
        choices=WebsiteRoleChoices,
        blank=True,
        help_text=_('Primary role of the web property, if applicable')
    )
    # prev names: public_ip_1 and private_ip_1
    public_ip_1 = models.GenericIPAddressField(
        _('Public IP (Orig)'), 
        blank=True, null=True, 
        protocol='IPv4',
        help_text='Public IP Address assigned for this web asset'
    )
    ipaddress_public_8 = models.ForeignKey(
        to='ipam.IPAddress',
        on_delete=models.SET_NULL,
        related_name='fqdns_public',
        blank=True, null=True,
        verbose_name='Public IP FK'
    )
    # private_ip_1 = models.GenericIPAddressField(
    #     _('Private IP (orig)'), 
    #     blank=True, null=True, protocol='IPv4',
    #     help_text='Primary internal IP of web server'
    # )
    # private_ip_2 = models.GenericIPAddressField(
    #     _('Private IP 2'),
    #     blank=True, null=True,
    #     protocol='IPv4',
    #     help_text='Secondary internal IP, e.g. VIP, NAT, or VLAN IPs'
    # )
    private_ip_1 = models.CharField(_('Private IP 1'), max_length=200, blank=True)
    private_ip_2 = models.CharField(_('Private IP 2'), max_length=200, blank=True)
    ipaddress_private_8 = models.ForeignKey(
        to='ipam.IPAddress',
        on_delete=models.SET_NULL,
        related_name='fqdns_private',
        blank=True, null=True,
        verbose_name='Private IP FK'
    )

    # Turn this into a ForeignKey
    # NOTE: Netbox appears to save hostname as "dns_name" field under IPAddress table, not separately
    # Original field name: hostname
    hostname_orig = models.CharField(_('Hostname orig'), max_length=100, blank=True, default='')

    # Turn this into a ForeignKey
    os_char = models.CharField(
        _('OS'), 
        max_length=100, 
        blank=True, default='', 
        help_text='OS (char field)'
    )
    os_1 = models.ForeignKey(
        to='OperatingSystem',
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True,
        verbose_name="OS My FK"
    )
    os_8 = models.ForeignKey(
        to='dcim.Platform',
        on_delete=models.SET_NULL,
        related_name='+',
        blank=True,
        null=True,
        verbose_name='OS Platform'
    )
    # Test - this is how Netbox ties contacts
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='fqdns',
        blank=True,
        null=True
    )
    # prev name: owners (and this used to be a TextField)
    owners_orig = models.TextField(_('Owners orig'), blank=True)
    owners_nb = GenericRelation(
        to='tenancy.ContactAssignment'
    )

    # owners_group = models.ForeignKey(
    #     to='tenancy.ContactGroup',
    #     on_delete=models.PROTECT,
    #     related_name='fqdns',
    #     blank=True, null=True,
    #     verbose_name='Owners Group',
    # )

    impacted_group_orig = models.ForeignKey(
        'BusinessGroup',
        on_delete=models.SET_NULL,
        related_name='fqdns',
        blank=True, null=True,
        verbose_name='Group orig'
    )
    impacted_division_orig = models.ForeignKey(
        'BusinessDivision',
        on_delete=models.SET_NULL,
        related_name='fqdns',
        blank=True, null=True,
        verbose_name='Division orig',
    )
    
    is_in_cmdb = models.BooleanField(
        _('In CMDB'), 
        null=True, 
        default=False,
        help_text='The asset is in official CMDB'
    )
    
    location_orig = models.ForeignKey(
        'SiteLocation',
        on_delete=models.SET_NULL, 
        blank=True, null=True,
        related_name='fqdns',
        verbose_name='Location orig'
    )
    
    location = models.ForeignKey(
        to='dcim.Site',
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='fqdns',
        verbose_name='Location',
    )
    # geo_region_orig = models.IntegerField(_('Geo Region orig'),
    #                               choices=GEO_REGION_CHOICES,
    #                               default=GEO_REGION_CHOICES.amer,
    #                               help_text='Geographic region site operates in (or Global)')

    geo_region_choice = models.CharField(
        _('Region choice'),
        max_length=50,
        choices=GeoRegionChoices,
        blank=True,
    )

    geo_region = models.ForeignKey(
        to='dcim.Region',
        on_delete=models.SET_NULL,
        related_name='fqdns',
        blank=True,
        null=True,
        verbose_name='Region NB',
    )

    # prev name: criticality_tmp1
    criticality_score_1 = models.PositiveSmallIntegerField(
        _('Criticality Score'),
        default=50,
        help_text='Rank asset criticality from 1-100 (least to most)'
    )

    # prev name: business_criticality
    # snow_bcdr_criticality = models.ForeignKey('BusinessCriticality',
    #                                          on_delete=models.PROTECT,
    #                                          blank=True, null=True,
    #                                          verbose_name='Business Criticality',
    #                                          help_text='SNOW CMDB-defined biz criticality')

    # env_used_for = models.IntegerField(_('Used For'),
    #                                      choices=SITE_ENV_CHOICES,
    #                                      default=SITE_ENV_CHOICES.production,
    #                                      help_text='Environment type the website is used for')
    # architectural_model = models.IntegerField(_('Hosting Model'),
    #                                           choices=CMDB_ARCH_MODEL,
    #                                           default=CMDB_ARCH_MODEL.hybrid)
    env_model = models.CharField(
        _('Environment Model'),
        max_length=100,
        choices=HostingEnvModelChoices,
        blank=True,
        help_text='The hosted SDLC environment primary model for this property (e.g. Prod, QA, Staging)'
    )
    architectural_model = models.CharField(
        _('Architectural Model'),
        max_length=100,
        choices=HostingArchModelChoices,
        blank=True,
        help_text='The hosted architecutral infrastructure model for this property (e.g. On-Premise, Cloud)'
    )
    tech_webserver_orig = models.CharField(
        _('Webserver Framework (orig)'),
        max_length=500,
        blank=True,
        help_text='Primary webserver framework operating on the asset property'
    )
    tech_webserver_1 = models.ForeignKey('WebserverFramework',
                                         on_delete=models.SET_NULL,
                                         blank=True, null=True,
                                         verbose_name='Webserver Tech-FK')

    tech_addtl = models.TextField(_('Addtl Tech'), blank=True, default='',
                                  help_text='Additional tech powering the site')
    
    # DNS Type Fields
    cnames = models.CharField(_('CNAMEs'), max_length=500, blank=True, default='')
    dns_a_record_ips = models.TextField(_("A-Records"), blank=True, default='')

    # TLS Details
    tls_cert_info = models.TextField(_('TLS Cert'), blank=True, default='',
                                     help_text='TLS Certificate info')
    tls_cert_expires = models.DateField(_('TLS Cert Expires'), blank=True, null=True,
                                        help_text='TLS Cert expiration date')
    tls_cert_sha1 = models.CharField(_('TLS Cert SHA1'), max_length=50, blank=True, default='')
    tls_cert_is_wildcard = models.BooleanField(_('Wildcard Cert'), null=True, default=None) # Default None makes these start as "Unknown"
    tls_version_int = models.IntegerField(
        _("TLS Version"), blank=True, null=True,
        choices=LAYER_SECURITY_CHOICES,
        default=None,
        help_text='SSL/TLS Protocol Version running based on recon results'
    )
    tls_protocol_version = models.CharField(
        _('TLS Protocol'),
        max_length=50,
        choices=TransportLayerSecurityVersionChoices,
        blank=True,
        help_text='TLS/SSL protocol version operating on this property, if applicable'
    )

    is_vhost = models.BooleanField(_('VHost'), null=True, default=False)
    is_http2 = models.BooleanField(_('HTTP2'), null=True, default=False)

    # prev name: status_code
    response_code = models.PositiveSmallIntegerField(_('Status Code'), blank=True, null=True,
                                                   help_text='Website response code')
    content_length = models.PositiveIntegerField(_('Content Length'), blank=True, null=True,
                                                 help_text='Website recon response content length size')

    # Note: These statuses would only be used if FqdnStatus is "3-Redirect"
    # redirect_status_orig = models.IntegerField(_('Redirect Health_9'),
    #                                       choices=REDIRECT_STATUS_CHOICES,
    #                                       blank=True, null=True)
    redirect_health = models.CharField(
        max_length=50,
        choices=RedirectStatusChoices,
        blank=True,
        verbose_name='Redirect Health',
        help_text='Website redirect health status, if applicable'
    )
    redirect_url = models.CharField(
        _('Redirect URL'), 
        max_length=1500, 
        blank=True, null=True,
        help_text=_('If applicable, the destination Redirect URL for this property')
    )
    # parked_status = models.ForeignKey('ParkedStatus',
    #                                   on_delete=models.PROTECT,
    #                                   blank=True, null=True,
    #                                   verbose_name='Parked Status')

    is_internet_facing = models.BooleanField(_('Internet Facing'), null=True, default=True)
    is_flagship = models.BooleanField(_('Flagship'), null=True, default=False)
    is_cloud_hosted = models.BooleanField(_('Cloud Hosted'), null=True, default=True)

    is_vendor_managed = models.BooleanField(_('Vendor Managed'), null=True, default=False)
    is_vendor_hosted = models.BooleanField(_('Vendor Hosted'), null=True, default=False)
    is_akamai = models.BooleanField(_('Akamai'), null=True, default=False)
    is_load_protected = models.BooleanField(_('Load Protected'), null=True, default=False)
    is_waf_protected = models.BooleanField(_('WAF Protected'), null=True, default=False)

    cloud_provider = models.CharField(
        _('Cloud Provider'),
        max_length=50,
        choices=CloudProviderChoices,
        blank=True,
    )

    # orig name: vendor_company_1
    vendor_company_orig = models.CharField(
        _('Vendor Name'), 
        max_length=150, 
        blank=True, 
    )
    # TODO: Not using yet
    vendor_company_fk = models.ForeignKey(
        to='Vendor',
        on_delete=models.PROTECT,
        related_name='fqdns',
        blank=True, null=True,
        verbose_name=_('Vendor Company (FK)'),
        help_text='Linked vendor company that is managing and/or hosting this property'
    )
    vendor_pocs_orig = models.CharField(
        _('Vendor POCs'), 
        max_length=500, 
        blank=True, 
        help_text='One or more vendor POCs that support this web property'
    )
    
    vendor_url = models.URLField(_('Vendor URL'), blank=True, null=True)
    vendor_notes = models.TextField(_('Vendor Notes'), blank=True, default='')

    website_url = models.URLField(_('Website URL'), max_length=400, blank=True, null=True)
    website_title = models.CharField(_('Website Title'), max_length=150, blank=True, default='')
    website_email_orig = models.EmailField(_('Site Email'), blank=True, default='')
    # website_screenshot = models.ImageField(upload_to=set_files_path, blank=True, null=True)
    # Device model uses this method for images
    website_homepage_image = models.ImageField(
        upload_to='wim-images',
        blank=True
    )
    images = GenericRelation(
        to='extras.ImageAttachment'
    )

    # -- Security
    # prev name: has_bb
    had_bugbounty = models.BooleanField(_('Had BB'), null=True, default=False,
                                        help_text="Property has had bug bounty submissions")
    # TODO: my guidance says don't do this, use NullBooleanField instead
    is_risky = models.BooleanField(_('Risky Site'), null=True, default=False,
                                   help_text='Is the website risky or known to have issues')

    site_operation_age = models.DateField(
        _('Operation Age'), 
        default=datetime.date.today,
        blank=True, null=True,
        help_text='Approx. year age of when site first came online (e.g. 2009-01-01)'
    )
    last_vuln_assessment = models.DateField(_('Last Vuln Assessment'), blank=True, null=True)
    vuln_scan_coverage = models.BooleanField(_('Vuln Scan Coverage'), null=True, default=False,
                                             help_text='Asset included in normal web vuln scanner coverage?')
    vuln_scan_last_date = models.DateField(_('Last Web Vuln Scan'), blank=True, null=True)
    vuln_assessment_priority = models.PositiveSmallIntegerField(
        _('Assessment Priority'),
        blank=True, null=True,
        help_text='Priority to test for vulnerabilities (1=Critical)'
    )

    risk_analysis_notes = models.TextField(_('Risk Notes'), blank=True, default='',
                                           help_text='Notes on why asset is broken or risky')
    # -- Feature tracking
    feature_acct_mgmt = models.BooleanField(
        _('Account Mgmt'), 
        null=True, default=False,
        help_text='Asset uses account management for access control'
    )
    
    # feature_auth_type = models.ForeignKey(
    #     'WebsiteAuthType', 
    #     on_delete=models.SET_NULL,
    #     blank=True, null=True
    # )
    feature_webauth_type = models.CharField(
        max_length=50,
        choices=WebAuthChoices,
        blank=True,
        verbose_name='Site Auth Type',
        help_text='Type of auth method employed for acct mgmt on this website'
    )
    feature_auth_self_registration = models.BooleanField(_('Self Registration'), null=True, default=False,
                                                         help_text='Account self-registration is enabled for anyone')
    feature_api = models.BooleanField(_('Feature: API'), null=True, default=False,
                                      help_text='Has an API accessible on the website')
    # -- Scoping Sizing
    scoping_size = models.PositiveSmallIntegerField(_('Content Size'), default=1,
                                                    help_text='Size of site (1-small to 3-large)')
    scoping_complexity = models.PositiveSmallIntegerField(_('Complexity'), default=1,
                                                          help_text='Complexity of site (1-simple to 3-complex')
    scoping_roles = models.PositiveSmallIntegerField(_('Test Roles'), default=0,
                                                     help_text='Number of roles with which to conduct security testing')
    
    @property
    def calc_loe(self):
        # Formula here
        if self.scoping_size:
            result = (self.scoping_size * 1.3) + (self.scoping_complexity * 1.4) + (self.scoping_roles * 1.4)
            return '{0:.1f}'.format(result)
    

    # Specific CMDB Type Fields We Also Need to Have
    # I made orig fields to temp store my orig values that were FK's before.
    # storing them at text until this is further built out using FK's to Tenancy
    support_group_website_technical_orig = models.CharField(
        _('Support Group Technical'),
        max_length=100,
        blank=True,
        help_text='Technical support group that can administer the webserver'
    )
    # support_group_website_technical = models.ForeignKey(
    #     'SupportGroup',
    #     verbose_name='Technical Support Group',
    #     on_delete=models.SET_NULL,
    #     related_name='fqdns_technical',
    #     blank=True, null=True
    # )

    support_group_website_approvals_orig = models.CharField(
        _('Support Group Business'),
        max_length=100,
        blank=True,
        help_text="Business owners responsible for decision making for the web property"
    )

    # support_group_website_approvals = models.ForeignKey(
    #     'SupportGroup',
    #     verbose_name='Business Support Group',
    #     on_delete=models.SET_NULL,
    #     related_name='fqdns_business',
    #     blank=True, null=True
    # )

    is_compliance_required = models.BooleanField(_('Compliance Required'), null=True, default=False)

    # compliance_programs = models.ManyToManyField(
    #     'ComplianceProgram', 
    #     blank=True, default='',
    #     related_name='fqdns'
    # )
    compliance_programs_choice = models.CharField(
        _('Compliance Programs'),
        max_length=50,
        choices=ComplianceProgramChoices,
        blank=True,
        help_text='If asset is beholden to one or more cybersecurity regulatory compliance programs',
    )
    

    # data_source_m2m = models.ManyToManyField('DataSource', blank=True,
    #                                          related_name='assets_m2m')
    # data_source = models.ForeignKey('DataSource', 
    #                                 blank=True, 
    #                                 null=True,
    #                                 on_delete=models.SET_NULL,
    #                                 verbose_name='Data Source')
    
    # TOOD: Renaming this to comments to match netbox?
    notes = models.TextField(_('Notes'), blank=True, default='')

    date_created = models.DateTimeField(_('Date Created'), 
                                        auto_now_add=True, 
                                        help_text='system field for creation date')
    date_modified = models.DateTimeField(_('Date Modified'), 
                                         auto_now=True, 
                                         help_text='system field for modified date')

    # def display_data_source_m2m(self):
    #     return ', '.join([data_source_m2m.name for data_source_m2m in self.data_source_m2m.all()])

    # --- custom managers for this model that can be accessed --
    # NOTE: admin takes the first model manager listed here as its default (unless we set it below)
    # objects = models.Manager()
    # Help: https://docs.djangoproject.com/en/4.1/topics/db/managers/
    #objects = ActiveAssetsManager()
    # active_records = ActiveAssetsManager()          # Asset.active_records.all()
    # active_fqdns = ActiveFQDNsAssetsManager()       # Asset.active_fqdns.all() - fqdn status is "5-Active"
    # only_websites = OnlyWebsitesManager()           # Asset.only_websites.all()

    # These are typically unique, we wouldn't have much reason to clone a record
    # clone_fields = (
    #     'name'
    # )

    # TODO: Important to define these? e.g. DeviceType defined dcim.Manufacturer
    # prerequisite_models = (
    #     'stuff',
    # )

    class Meta:
        #default_manager_name =
        ordering = ['name']
        verbose_name = _('FQDN')
        verbose_name_plural = _('FQDNs')
        #default_manager_name = 'active_fqdns'       # This is my default, unless I'm troubleshooting or doing something non-standard
        # indexes = [
        #     models.Index(fields=['name']),
        # ]
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wim:fqdn', args=[self.pk])

    # NOTE: You must define a function if you want colored labels for a field
    #       in the table "ListView" view
    def get_status_color(self):
        return FQDNStatusChoices.colors.get(self.status)
    
    def get_fqdn_status_color(self):
        return FQDNOpsStatusChoices.colors.get(self.fqdn_status)
    
    def get_website_status_color(self):
        return WebsiteOpsStatusChoices.colors.get(self.website_status)
    
    def get_asset_confidence_color(self):
        return AssetConfidenceChoices.colors.get(self.asset_confidence)
    
    def get_asset_class_color(self):
        return AssetClassChoices.colors.get(self.asset_class)
    
    def get_role_color(self):
        return WebsiteRoleChoices.colors.get(self.website_role)
