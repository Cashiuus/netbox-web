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
    'DomainForm',
    'FQDNForm',
    'BusinessDivisionForm',
    'BusinessGroupForm',
    'OperatingSystemForm',
    'SiteLocationForm',
    'VendorForm',
    'WebserverFrameworkForm',
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

    # -- FKs --
    # registrar_company = DynamicModelChoiceField(
    #     queryset=Registrar.objects.all(),
    #     required=True,
    #     selector=True,
    # )

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
            'tenant', 'ownership_type',
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
    )
    # TODO: forms.RadioSelect doesn't seem to work, doesn't 
    #       show up on website form
    # asset_confidence = forms.RadioSelect(
    #     choices=AssetConfidenceChoices,
    # )
    asset_confidence = forms.ChoiceField(
        choices=AssetConfidenceChoices,
        required=False,
        label=_('Asset Confidence'),
    )
    
    fqdn_status = forms.ChoiceField(
        choices=FQDNOpsStatusChoices,
        label=_('FQDN Tech Status')
    )
    # website_status = forms.ChoiceField(
    #     choices=WebsiteOpsStatusChoices,
    # )
    
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
        choices=CloudProviderChoices,
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
    
    # -- Bools --
    mark_triaging = forms.BooleanField(
        required=False,
        label=_('Triaging'),
    )
    # TODO: I'd really like to have whatever value is current and then
    # just don't change it if i don't modify. For that, think it must be a drop-down
    # or maybe a radio select widget
    is_internet_facing = forms.BooleanField(
        required=False,
        initial=True,
    )

    # -- FKs --
    domain = DynamicModelChoiceField(
        queryset=Domain.objects.all(),
        required=True,
        selector=True,
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

    # TODO: Improve upon this, it just looks like a box to type in, 
    # doesn't connect to the IPAddress FK
    # ipaddress_public_8 = IPNetworkFormField(required=False)
    # ipaddress_private_8 = IPNetworkFormField(required=False)

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
    tech_webserver_1 = DynamicModelChoiceField(
        queryset=WebserverFramework.objects.all(),
        required=False,
        label=_('Webserver Framework (FK)'),
    )

    # vendor_company_1 = DynamicModelChoiceField(
    #     queryset=Vendor.objects.all(),
    #     required=False,
    #     label=_('Vendor Company (FK)'),
    # )

    # -- Booleans --
    had_bugbounty = forms.BooleanField(required=False)
    is_risky = forms.BooleanField(required=False)
    is_in_cmdb = forms.BooleanField(required=False, label=_('In CMDB'))
    is_compliance_required = forms.BooleanField(
        required=False,
        label=_('Is Compliance Required'),
    )
    is_internet_facing = forms.BooleanField(required=False)
    is_flagship = forms.BooleanField(required=False)
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
    # scan_fingerprint_json = JSONField(required=False)

    fieldsets = (
        ("FQDN", (
            "name", "mark_triaging", "asset_confidence",
            "status", "status_reason",
            "fqdn_status", "website_status",
            "asset_class", "domain",
            'env_model', 'architectural_model',
            "geo_region_choice",
            "geo_region",
            "location_orig", "location",
            "is_in_cmdb", 'is_flagship',

        )),
        ("Tenancy", (
            "impacted_group_orig", "impacted_division_orig",
            "owners_orig", "tenant",
            'support_group_website_technical_orig', 'support_group_website_approvals_orig',
        )),
        ("Technical Details", (
            "public_ip_1", "ipaddress_public_8",
            'is_internet_facing',
            'is_cloud_hosted', 'cloud_provider',
            'tech_webserver_orig', 'tech_webserver_1', 'tech_addtl',
            'private_ip_1', 'private_ip_2',
            # 'ipaddress_private_8', 
            'hostname_orig',
            'os_char',
            'os_1', 'os_8',
            'website_url', 'website_title', 'website_email_orig',
            'website_role',
            'site_operation_age',
            'redirect_health', 'redirect_url',
        )),
        ("Security", (
            'criticality_score_1',
            'vuln_assessment_priority',
            'had_bugbounty', 'is_risky',
            # 'is_compliance_required', 'compliance_programs',
            'is_akamai', 'is_load_protected', 'is_waf_protected',
            'vuln_scan_coverage', 'vuln_scan_last_date',
            'last_vuln_assessment',
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
            'vendor_company_orig', 'vendor_pocs_orig', 'vendor_notes',
        )),
        ("TLS", (
            'tls_protocol_version', 'tls_cert_expires',
            'tls_cert_info', 'tls_cert_sha1', 'tls_cert_is_wildcard',
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
            "name", "mark_triaging", "asset_confidence",
            "status", "status_reason",
            'fqdn_status', 'website_status',
            'asset_class', 'domain',
            'impacted_group_orig', 'impacted_division_orig',
            'location_orig', 'location',
            'geo_region_choice', 'geo_region',
            'env_model', 'architectural_model',
            'public_ip_1', 'ipaddress_public_8',
            'tech_webserver_orig', 'tech_webserver_1', 'tech_addtl',
            'is_in_cmdb', 'is_flagship',
            'is_internet_facing',
            'is_akamai', 'is_load_protected', 'is_waf_protected',
            'tenant', 'owners_orig',
            'support_group_website_technical_orig', 'support_group_website_approvals_orig',
            'private_ip_1', 'private_ip_2',
            # 'ipaddress_private_8', 
            'hostname_orig',
            'os_char', 
            'os_1', 'os_8',
            'criticality_score_1',
            'tls_protocol_version', 'tls_cert_expires',
            'tls_cert_info', 'tls_cert_sha1', 'tls_cert_is_wildcard',
            'website_url', 'website_title', 'website_email_orig',
            'site_operation_age',
            'redirect_health', 'redirect_url',
            'had_bugbounty', 'is_risky',
            'vuln_scan_coverage', 'vuln_scan_last_date',
            'last_vuln_assessment', 'vuln_assessment_priority',
            'risk_analysis_notes', 'scan_fingerprint_json',
            
            'is_cloud_hosted', 'cloud_provider',
            'is_vendor_managed', 'is_vendor_hosted',
            'vendor_company_orig', 
            'vendor_pocs_orig',
            'vendor_notes',
            
            'feature_api',
            'feature_acct_mgmt', 'feature_webauth_type', 'feature_auth_self_registration',
            # Scoping --
            'scoping_size', 'scoping_complexity', 'scoping_roles',
            'is_compliance_required', 'compliance_programs_choice',
            'notes',
            'tags',
        ]


class BusinessGroupForm(NetBoxModelForm):

    class Meta:
        model = BusinessGroup
        fields = ['name', 'acronym']


class BusinessDivisionForm(NetBoxModelForm):

    class Meta:
        model = BusinessDivision
        fields = ['name', 'acronym', 'group']


class OperatingSystemForm(NetBoxModelForm):

    class Meta:
        model = OperatingSystem
        fields = (
            'vendor', 'product', 'update',
            'platform_family', 'platform_type',
            'build_number', 'cpe', 'color',
        )


class SiteLocationForm(NetBoxModelForm):

    class Meta:
        model = SiteLocation
        fields = [
            'name', 'code', 
            'impacted_group_orig', 'impacted_division_orig',
            'geo_region_choice',
            'geo_region', 'tenant',
        ]


class VendorForm(NetBoxModelForm):

    class Meta:
        model = Vendor
        fields = (
            'name',
        )


class WebserverFrameworkForm(NetBoxModelForm):
    slug = SlugField()

    class Meta:
        model = WebserverFramework
        fields = (
            'name', 'slug', 'product', 'version', 
            'raw_banner', 'cpe',
            'order',
        )
