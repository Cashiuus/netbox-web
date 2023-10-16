from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from netbox.forms import NetBoxModelForm
from tenancy.forms import TenancyForm
from utilities.exceptions import PermissionsViolation
from utilities.forms import BootstrapMixin, add_blank_choice
from utilities.forms.fields import (
    CommentField, ContentTypeChoiceField,
    DynamicModelChoiceField, DynamicModelMultipleChoiceField,
    JSONField,
    NumericArrayField,
    SlugField,
)
from utilities.forms.widgets import DatePicker, ClearableFileInput
from dcim.models import Device, Interface, Location, Platform, Rack, Region, Site, SiteGroup

# from dcim.models import Platform
from ipam.formfields import IPNetworkFormField
from ipam.models import *
# from ipam.models import IPAddress
from wim.choices import *
from wim.constants import *
from wim.models import *


__all__ = (
    'BrandForm',
    'DomainForm',
    'FQDNForm',
    'BusinessDivisionForm',
    'BusinessGroupForm',
    'OperatingSystemForm',
    'SiteLocationForm',
    'VendorForm',
    'WebEmailForm',
    'SoftwareForm',
)


class DomainForm(TenancyForm, NetBoxModelForm):

    # -- Choices --
    status = forms.ChoiceField(
        choices=DomainStatusChoices,
        help_text=_('Domain root operational status')
    )
    asset_confidence = forms.ChoiceField(
        choices=AssetConfidenceChoices,
        required=False,
        help_text=_('Domain attribution confidence level')
    )
    ownership_type = forms.ChoiceField(
        choices=DomainOwnershipStatusChoices,
        required=False,
    )

    # -- Bools --
    is_internet_facing = forms.BooleanField(required=False)
    is_flagship = forms.BooleanField(required=False)
    # meets_standards = forms.BooleanField(required=False)

    # -- FKs --
    # registrar_company = DynamicModelChoiceField(
    #     queryset=Registrar.objects.all(),
    #     required=True,
    #     selector=True,
    # )
    brand = DynamicModelChoiceField(
        queryset=Brand.objects.all(),
        required=False,
        selector=True,
        label=_('Brand/Acquisition'),
    )

    # -- M2M --
    registration_emails = DynamicModelMultipleChoiceField(
        queryset=WebEmail.objects.all(),
        required=False,
        label=_('Registration Emails'),
        to_field_name='email_address',
        help_text='List of all email addresses in domain registration, comma-separated'
    )

    # fieldsets = (
    # )

    class Meta:
        model = Domain
        fields = [
            'name', 'status', 'asset_confidence',
            'tenant', 'ownership_type', 'brand',
            'is_internet_facing', 'is_flagship',
            'meets_standards',
            'date_registrar_expiry', 'date_first_registered',
            'date_last_recon_scanned',
            'registrar_company_orig', 'registrar_iana_id_orig',
            'registrant_org',
            'registration_emails_orig', 'registration_emails',
            'nameservers', 'mail_servers', 'whois_servers',
            'soa_nameservers', 'soa_email',
            'registrar_domain_statuses',
            'notes',
        ]




class FQDNForm(TenancyForm, NetBoxModelForm):
    # -- Choices --
    status = forms.ChoiceField(
        choices=FQDNStatusChoices,
        required=False,
    )
    asset_class = forms.ChoiceField(
        choices=AssetClassChoices,
        required=False,
        widget=forms.RadioSelect,
        label=_('Asset Class'),
    )
    asset_confidence = forms.ChoiceField(
        choices=AssetConfidenceChoices,
        required=False,
        label=_('Asset Confidence'),
    )
    fqdn_status = forms.ChoiceField(
        choices=FQDNOpsStatusChoices,
        required=False,
        label=_('FQDN Tech Status')
    )
    website_status = forms.ChoiceField(
        choices=WebsiteOpsStatusChoices,
        required=False,
        label=_('Website Status'),
    )
    # website_role = forms.ChoiceField(
    #     choices=add_blank_choice(WebsiteRoleChoices),
    #     required=False,
    # )
    # web_auth_type = forms.ChoiceField(
    #     choices=WebAuthChoices,
    #     required=False
    # )
    geo_region_choice = forms.ChoiceField(
        choices=GeoRegionChoices,
        required=False,
    )
    cloud_provider = forms.ChoiceField(
        choices=add_blank_choice(CloudProviderChoices),
        required=False,
        label=_('Cloud Provider'),
    )
    compliance_programs_choice = forms.ChoiceField(
        choices=ComplianceProgramChoices,
        required=False,
        label=_('Compliance Programs'),
    )

    # -- Numbers --
    criticality_score_1 = forms.IntegerField(
        min_value=1,
        max_value=100,
        required=False,
        label=_('Criticality Score'),
        help_text=_('Asset criticality score for prioritization (1=low, 100=critical)')
    )
    scoping_size = forms.IntegerField(
        required=False,
    )
    scoping_complexity = forms.IntegerField(
        required=False,
    )
    scoping_roles = forms.IntegerField(
        required=False,
    )

    # -- FKs --
    domain = DynamicModelChoiceField(
        queryset=Domain.objects.all(),
        required=False,
        selector=True,
        label=_('Parent Domain'),
    )
    ipaddress_public_8 = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        selector=True,
        label=_('Public IP (NB)'),
    )
    ipaddress_private_8 = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        selector=True,
        label=_('Private IP (NB)'),
    )
    # os_1 = DynamicModelChoiceField(
    #     queryset=OperatingSystem.objects.all(),
    #     required=False,
    #     selector=True,
    #     label=_("OS (My FK)")
    # )
    os_8 = DynamicModelChoiceField(
        queryset=Platform.objects.all(),
        required=False,
        selector=True,
        label=_('OS (NB)')
    )
    impacted_group_orig = DynamicModelChoiceField(
        queryset=BusinessGroup.objects.all(),
        required=False,
        selector=True,
        label=_('Bus. Group (Orig)'),
    )
    impacted_division_orig = DynamicModelChoiceField(
        queryset=BusinessDivision.objects.all(),
        required=False,
        selector=True,
        label=_('Bus. Division (Orig)'),
    )
    location_orig = DynamicModelChoiceField(
        queryset=SiteLocation.objects.all(),
        required=False,
        selector=True,
        label=_('Site Location (Orig)')
    )
    location = DynamicModelChoiceField(
        # If i use facility, I probably have edit this to pull 'facility' also...
        queryset=Site.objects.all(),
        required=False,
        # TODO: When I enable this, the drop-down still populates with "name" and can't save
        # to_field_name="facility",
        label=_('Site Location (NB)'),
    )
    geo_region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('Geo Region (NB)'),
        # initial_params={
        #     "sites":
        # }
    )
    vendor_company_fk = DynamicModelChoiceField(
        queryset=Vendor.objects.all(),
        required=False,
        label=_('Vendor Company (FK)'),
    )

    # -- M2M --
    software = DynamicModelMultipleChoiceField(
        queryset=Software.objects.all(),
        required=False,
        label=_('Software'),
    )

    # -- Booleans --
    mark_triaging = forms.BooleanField(
        required=False,
        label=_('Triaging'),
    )
    # TODO: I'd really like to have whatever value is current and then
    # just don't change it if i don't modify. For that, I think it must
    # be a drop-down or maybe a radio select widget
    is_internet_facing = forms.BooleanField(required=False, initial=True)
    had_bugbounty = forms.BooleanField(required=False)
    is_risky = forms.BooleanField(required=False)
    is_in_cmdb = forms.BooleanField(required=False, label=_('In CMDB'))
    is_compliance_required = forms.BooleanField(
        required=False,
        label=_('Is Compliance Required'),
    )
    is_internet_facing = forms.BooleanField(required=False)
    is_flagship = forms.BooleanField(required=False)
    is_nonprod_mirror = forms.BooleanField(required=False)
    is_cloud_hosted = forms.BooleanField(required=False)
    # is_vendor_managed = forms.BooleanField(required=False)
    # is_vendor_hosted = forms.BooleanField(required=False)
    is_akamai = forms.BooleanField(required=False)
    is_load_protected = forms.BooleanField(required=False)
    is_waf_protected = forms.BooleanField(required=False)
    is_vhost = forms.BooleanField(required=False)
    is_http2 = forms.BooleanField(required=False)
    tls_cert_is_wildcard = forms.BooleanField(required=False)

    # -- JSON fields --
    scan_fingerprint_json = JSONField(required=False, label='Scan Fingerprint')

    fieldsets = (
        ("FQDN", (
            "name", "mark_triaging",
            "status", "status_reason",
            "asset_confidence",
            "fqdn_status", "website_status",
            "date_last_recon",
            "asset_class", "domain",
            'env_model', 'architectural_model',
            "geo_region_choice", "geo_region",
            "location_orig", "location",
            'is_internet_facing', 'is_nonprod_mirror',
            'is_flagship', "is_in_cmdb",
            'is_cloud_hosted', 'cloud_provider',
        )),
        ("Tenancy", (
            "impacted_group_orig", "impacted_division_orig",
            "tenant",
            "owners_orig",
            'support_group_website_technical_orig', 'support_group_website_approvals_orig',
        )),
        ("Technical Details", (
            "public_ip_1", "ipaddress_public_8",
            'private_ip_1', 'private_ip_2',
            # 'ipaddress_private_8',
            'hostname_orig',
            'os_char',
            'os_1', 'os_8',
            'website_url', 'website_title', 'website_email_orig',
            'website_role',
            'site_operation_age',
            'redirect_health', 'redirect_url',
            'software',
            'tech_webserver_orig', 'tech_addtl',
            "cnames", "dns_a_record_ips",
        )),
        ("Security", (
            'criticality_score_1',
            'vuln_assessment_priority',
            'had_bugbounty', 'is_risky',
            # 'is_compliance_required', 'compliance_programs',
            'is_akamai', 'is_load_protected', 'is_waf_protected',
            'vuln_scan_coverage', 'vuln_scan_last_date',
            # 'last_vuln_assessment',
            'risk_analysis_notes',
            'scan_fingerprint_json',
        )),
        ("Scoping", (
            'feature_api',
            'feature_acct_mgmt', 'feature_webauth_type', 'feature_auth_self_registration',
            'scoping_size', 'scoping_complexity', 'scoping_roles',
        )),
        ("Vendor", (
            'is_vendor_managed', 'is_vendor_hosted',
            'vendor_company_fk',
            'vendor_company_orig', 'vendor_pocs_orig',
            'vendor_url', 'vendor_notes',
        )),
        ("TLS", (
            'tls_protocol_version', 'tls_cert_expires',
            'tls_cert_info', 'tls_cert_sha1', 'tls_cert_is_wildcard',
            #'tls_cert_self_signed',
        )),
        (None, (
            "notes", "tags",
        )),
    )

    class Meta:
        model = FQDN
        widgets = {
            'website_homepage_image': ClearableFileInput(attrs={
                'accept': WEBSITE_IMAGE_FORMATS
            })
        }
        fields = [
            "name", "mark_triaging",
            "asset_confidence",
            "status", "status_reason",
            'fqdn_status', 'website_status',
            "date_last_recon",
            'asset_class', 'domain',
            'impacted_group_orig', 'impacted_division_orig',
            'location_orig', 'location',
            'geo_region_choice', 'geo_region',
            'env_model', 'architectural_model',
            'public_ip_1', 'ipaddress_public_8',
            'is_internet_facing', 'is_nonprod_mirror',
            'is_flagship', "is_in_cmdb",
            'is_akamai', 'is_load_protected', 'is_waf_protected',
            'tenant', 'owners_orig',
            'support_group_website_technical_orig', 'support_group_website_approvals_orig',
            'private_ip_1', 'private_ip_2',
            # 'ipaddress_private_8',
            'hostname_orig',
            'os_char',
            'os_1', 'os_8',
            'criticality_score_1',

            'website_url', 'website_title', 'website_email_orig',
            'site_operation_age',
            'redirect_health', 'redirect_url',
            'software',
            'tech_webserver_orig', 'tech_addtl',
            "cnames", "dns_a_record_ips",
            'had_bugbounty', 'is_risky',
            'vuln_scan_coverage', 'date_last_vulnscan',
            'date_last_pentest', 'pentest_priority',
            'risk_analysis_notes', 'scan_fingerprint_json',

            'is_cloud_hosted', 'cloud_provider',
            'is_vendor_managed', 'is_vendor_hosted',
            'vendor_company_fk', 'vendor_company_orig',
            'vendor_pocs_orig',
            'vendor_notes',

            'feature_api',
            'feature_acct_mgmt', 'feature_webauth_type', 'feature_auth_self_registration',
            # Scoping --
            'scoping_size', 'scoping_complexity', 'scoping_roles',
            'is_compliance_required', 'compliance_programs_choice',

            'tls_protocol_version', 'tls_cert_expires',
            'tls_cert_info', 'tls_cert_sha1', 'tls_cert_is_wildcard',
            'tls_cert_self_signed',
            'notes',
            'tags',
        ]


class BrandForm(NetBoxModelForm):

    slug = SlugField()

    class Meta:
        model = Brand
        fields = ['name', 'slug', 'description']


class BusinessGroupForm(NetBoxModelForm):

    slug = SlugField()

    class Meta:
        model = BusinessGroup
        fields = ['name', 'acronym', 'slug']


class BusinessDivisionForm(NetBoxModelForm):

    slug = SlugField()

    class Meta:
        model = BusinessDivision
        fields = ['name', 'acronym', 'slug', 'group']


class OperatingSystemForm(NetBoxModelForm):

    slug = SlugField()

    class Meta:
        model = OperatingSystem
        fields = (
            'vendor', 'slug', 'product', 'update',
            'platform_family', 'platform_type',
            'build_number', 'cpe', 'color',
        )


class SiteLocationForm(NetBoxModelForm):

    slug = SlugField()

    class Meta:
        model = SiteLocation
        fields = [
            'name', 'code', 'slug', 'active',
            'impacted_group_orig', 'impacted_division_orig',
            'geo_region_choice',
            'geo_region', 'tenant',
        ]


class VendorForm(NetBoxModelForm):

    slug = SlugField()

    class Meta:
        model = Vendor
        fields = (
            'name', 'slug',
            'description',
            'url',
            # Cannot include 'contacts' here because it is a read-only field
            'vendor_pocs_orig', 'notes',
        )


class WebEmailForm(NetBoxModelForm):

    class Meta:
        model = WebEmail
        fields = (
            'email_address',
        )


class SoftwareForm(NetBoxModelForm):
    slug = SlugField()

    class Meta:
        model = Software
        fields = (
            'name', 'slug', 'product', 'version',
            'raw_banner', 'cpe',
            'order',
        )
