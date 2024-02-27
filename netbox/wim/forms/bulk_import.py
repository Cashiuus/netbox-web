import json

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from dcim.models import Site, Region
from ipam.models import IPAddress
from wim.choices import *
from wim.constants import *
from wim.models import *
from netbox.forms import NetBoxModelImportForm
from tenancy.models import Tenant
from utilities.choices import ImportFormatChoices
from utilities.forms.fields import (
    CSVChoiceField, CSVContentTypeField, CSVModelChoiceField, CSVModelMultipleChoiceField, CSVTypedChoiceField,
    SlugField,
)


__all__ = (
    'BrandImportForm',
    'BusinessGroupImportForm',
    'BusinessDivisionImportForm',
    'CertificateImportForm',
    'DomainImportForm',
    'FQDNImportForm',
    'OperatingSystemImportForm',
    'SiteLocationImportForm',
    'SoftwareImportForm',
    'VendorImportForm',
)


#
# Brands
#
class BrandImportForm(NetBoxModelImportForm):
    slug = SlugField()

    class Meta:
        model = Brand
        fields =  ('name', 'slug')


#
# BusinessGroups
#
class BusinessGroupImportForm(NetBoxModelImportForm):
    # -- FKs --
    # principal_location_orig = CSVModelChoiceField(
    #     queryset = SiteLocation.objects.all(),
    #     to_field_name="code",
    # )
    # principal_location_nb = CSVModelChoiceField(
    #     queryset=Site.objects.all(),
    #     to_field_name='name',
    # )

    slug = SlugField()

    class Meta:
        model = BusinessGroup
        fields = (
            'name', 'slug', 'acronym', 'description',
            'principal_location_orig', 'principal_location_nb',
        )


#
# BusinessDivisions
#
class BusinessDivisionImportForm(NetBoxModelImportForm):
    # -- FKs --
    group = CSVModelChoiceField(
        queryset=BusinessGroup.objects.all(),
        required=True,
        to_field_name="acronym",
        help_text='Linked/Parent Business group acronym'
    )
    principal_location_orig = CSVModelChoiceField(
        queryset=SiteLocation.objects.all(),
        to_field_name='code',
        required=False,
        help_text='Linked site location code'
    )

    class Meta:
        model = BusinessDivision
        fields = (
            'name', 'slug', 'acronym', 'group', 'description',
            'principal_location_orig',
        )


#
# Certificates
#
class CertificateImportForm(NetBoxModelImportForm):
    # -- Choices --
    signing_algorithm = CSVChoiceField(
        choices=CertSigningAlgorithmChoices,
        required=False,
        help_text=_('Cert key signing algorithm used'),
    )
    key_type = CSVChoiceField(
        choices=CertKeyTypeChoices,
        required=False,
        help_text=_('Cert key signing algorithm used'),
    )
    key_bitlength = CSVChoiceField(
        choices=CertBitLengthChoices,
        required=False,
        help_text=_('Cert key signing algorithm used'),
    )
    class Meta:
        model = Certificate
        fields = (
            "hash_sha1",
            "hash_sha256", "hash_md5",
            "date_issued", "date_expiration",
            "sdn", "scn", "san", "sorg",
            "idn", "icn", "iorg", "signing_algorithm",
            "key_type", "key_bitlength", "is_wildcard", "is_self_signed",
        )


#
# Domains
#
class DomainImportForm(NetBoxModelImportForm):
    # -- Choices Fields --
    status = CSVChoiceField(
        choices=DomainStatusChoices,
        required=False,
        help_text=_('Domain root operational status'),
    )
    asset_confidence = CSVChoiceField(
        choices=AssetConfidenceChoices,
        required=False,
        help_text=_('Domain attribution confidence level'),
    )
    ownership_type = CSVChoiceField(
        choices=DomainOwnershipStatusChoices,
        required=False,
        help_text=_('Ownership type for this domain'),
    )

    # -- Bools --
    is_flagship = forms.BooleanField(
        required=False,
    )
    is_internet_facing = forms.BooleanField(
        required=False,
    )
    meets_standards = forms.BooleanField(
        required=False,
    )

    # -- FKs --
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Assigned tenant')
    )
    brand = CSVModelChoiceField(
        queryset=Brand.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Brand/Acquisition')
    )

    # registrar_company = CSVModelChoiceField(
    #     queryset=Registrar.objects.all(),
    #     required=False,
    #     to_field_name='name',
    #     # help_text=_('Regisrar company name')
    # )

    # -- M2M Fields --
    # TODO: Unsure how to configure a ManyToMany field for bulk import
    registration_emails = CSVModelMultipleChoiceField(
        queryset=WebEmail.objects.all(),
        required=False,
        to_field_name='email_address',
        help_text='List of all email addresses in domain registration, comma-separated'
    )

    class Meta:
        model = Domain
        # fields = ('name', 'tenant')
        fields = (
            'name', 'status', 'asset_confidence', 'ownership_type',
            'meets_standards',
            'tenant', 'brand',
            'date_registrar_expiry', 'date_first_registered',
            'date_last_recon_scanned',
            'is_internet_facing', 'is_flagship',
            'registrar_company_orig', 'registrar_iana_id_orig',
            'registrar_domain_statuses',
            'registrant_org',
            'registration_emails_orig', 'registration_emails',
            'nameservers', 'mail_servers', 'whois_servers',
            'soa_nameservers', 'soa_email',
            'notes',
        )


#
#   FQDN
#
class FQDNImportForm(NetBoxModelImportForm):
    # -- Choices Fields --
    status = CSVChoiceField(
        choices=FQDNStatusChoices,
        required=False,
        help_text=_('Overall ops status choices')
    )
    status_reason = CSVChoiceField(
        choices=AssetStatusReasonChoices,
        required=False,
        help_text=_('The reason for the current asset status, if applicable')
    )
    asset_confidence = CSVChoiceField(
        choices=AssetConfidenceChoices,
        required=False,
        help_text=_('Asset attribution confidence determination')
    )
    fqdn_status = CSVChoiceField(
        choices=FQDNOpsStatusChoices,
        required=False,
        help_text=_('FQDN operational status choices')
    )
    website_status = CSVChoiceField(
        choices=WebsiteOpsStatusChoices,
        required=False,
        help_text=_('Website operational status choices')
    )
    website_role = CSVChoiceField(
        choices=WebsiteRoleChoices,
        required=False,
        help_text=_('Primary website role or purpose, if applicable')
    )
    asset_class = CSVChoiceField(
        choices=AssetClassChoices,
        required=False,
        help_text=_('Class of web property asset')
    )
    env_model = CSVChoiceField(
        choices=HostingEnvModelChoices,
        required=False,
        help_text=_('The hosted SDLC environment primary model for this property (e.g. Prod, QA, Staging)')
    )
    architectural_model = CSVChoiceField(
        choices=HostingArchModelChoices,
        required=False,
        help_text=_('The hosted architecutral infrastructure model for this property (e.g. On-Premise, Cloud)')
    )
    geo_region_choice = CSVChoiceField(
        choices=GeoRegionChoices,
        required=False,
        help_text=_('Geographic region for this web property')
    )
    cloud_provider = CSVChoiceField(
        choices=CloudProviderChoices,
        required=False,
        help_text=_('For cloud assets, the associated cloud provider')
    )
    tls_protocol_version = CSVChoiceField(
        choices=TransportLayerSecurityVersionChoices,
        required=False,
        help_text=_('The TLS/SSL protocol version running on this property, if applicable'),
    )
    redirect_health = CSVChoiceField(
        choices=RedirectStatusChoices,
        required=False,
        help_text=_('The health status of redirect config, if this property is setup as a redirect'),
    )
    feature_webauth_type = CSVChoiceField(
        choices=WebAuthChoices,
        required=False,
        help_text=_('Type of auth method employed by the website, if applicable'),
    )
    compliance_programs_choice = CSVChoiceField(
        choices=ComplianceProgramChoices,
        required=False,
        help_text=_('One or more compliance program requirements in-scope for this asset'),
    )

    # -- Numbers Fields --
    criticality_score_1 = forms.IntegerField(
    #     min_value=1,
    #     max_value=100,
        required=False,
        help_text=_('Asset criticality score for prioritization (1=low, 100=critical)'),
    )
    scoping_size = forms.IntegerField(required=False)
    scoping_complexity = forms.IntegerField(required=False)
    scoping_roles = forms.IntegerField(required=False)

    # -- Bools --
    mark_triaging = forms.BooleanField(
        required=False,
        help_text=_('Is the asset marked for triaging focus currently'),
    )
    is_risky = forms.BooleanField(
        required=False,
        help_text=_('True if property has been determined to be insecure or risky'),
    )
    had_bugbounty = forms.BooleanField(
        required=False,
        help_text=_('True if property was associated with known bug bounty submissions'),
    )
    is_flagship = forms.BooleanField(
        required=False,
    )
    is_in_cmdb = forms.BooleanField(
        required=False,
    )
    is_nonprod_mirror = forms.BooleanField(
        required=False,
    )
    is_cloud_hosted = forms.BooleanField(
        required=False,
    )
    is_akamai = forms.BooleanField(
        required=False,
    )
    is_load_protected = forms.BooleanField(
        required=False,
    )
    is_waf_protected = forms.BooleanField(
        required=False,
    )
    is_internet_facing = forms.BooleanField(
        required=False,
    )
    is_vhost = forms.BooleanField(
        required=False,
    )
    is_http2 = forms.BooleanField(
        required=False,
    )
    is_vendor_managed = forms.BooleanField(
        required=False,
    )
    is_vendor_hosted = forms.BooleanField(
        required=False,
    )
    feature_acct_mgmt = forms.BooleanField(
        required=False,
    )
    feature_auth_self_registration = forms.BooleanField(
        required=False,
    )
    feature_api = forms.BooleanField(
        required=False,
    )
    is_compliance_required = forms.BooleanField(
        required=False,
    )
    tls_cert_is_wildcard = forms.BooleanField(
        required=False,
    )

    # -- FK Fields --
    domain = CSVModelChoiceField(
        queryset=Domain.objects.all(),
        to_field_name='name',
        required=False,
        help_text=_('Parent domain for this asset')
    )
    certificate = CSVModelChoiceField(
        queryset=Certificate.objects.all(),
        to_field_name='hash_sha1',
        required=False,
        help_text=_('TLS Certificate SHA1 hash running on this resource')
    )
    impacted_group_orig = CSVModelChoiceField(
        queryset=BusinessGroup.objects.all(),
        to_field_name="acronym",
        required=False,
        help_text=_('The impacted business group owning this property')
    )
    impacted_division_orig = CSVModelChoiceField(
        queryset=BusinessDivision.objects.all(),
        to_field_name="acronym",
        required=False,
        help_text=_('The impacted business division owning this property')
    )
    geo_region = CSVModelChoiceField(
        queryset=Region.objects.all(),
        to_field_name="name",
        required=False,
        help_text=_('Geographic region linked to org model')
    )
    location_orig = CSVModelChoiceField(
        queryset=SiteLocation.objects.all(),
        to_field_name="code",
        required=False,
        help_text=_('Assigned site location code'),
    )
    location = CSVModelChoiceField(
        queryset=Site.objects.all(),
        # TODO: I may want to re-do how I did this, and import all sites
        # so that the acronym is in the "name" field...
        to_field_name="facility",
        required=False,
        help_text=_('Assigned tenancy site code'),
    )
    vendor_company_fk = CSVModelChoiceField(
        queryset=Vendor.objects.all(),
        to_field_name='name',
        required=False,
        help_text=_('Vendor hosting or managing this property (FK)'),
    )
    ipaddress_public_8 = CSVModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        to_field_name='address',
        help_text=_('Public IP address FK linked to IPAM')
    )
    # ipaddress_private_8 = CSVModelChoiceField(
    #     queryset=IPAddress.objects.all(),
    #     required=False,
    #     to_field_name='address',
    #     help_text=_('Private IP address linked to IPAM')
    # )
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Assigned tenant')
    )

    # -- M2M Fields --
    # Basing this off VirtualDeviceContext M2M from dcim/forms/bulk_import.py
    software = CSVModelMultipleChoiceField(
        queryset=Software.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Software names and versions separated by commas, encased in double-quotes'),
    )

    # -- JSON or Data type fields --
    # scan_fingerprint_json = forms.CharField(
    #     required=False,
    #     widget=forms.Textarea(attrs={'class': 'font-monospace'}),
    #     help_text=_('Enter scan fingerprint in JSON format'),
    # )

    class Meta:
        model = FQDN
        # exclude = ('id',)
        # import_id_fields = ['name',]      # This doesn't exist. I'll have to build it
        fields = (
            "name", "id",
            "mark_triaging", "asset_confidence",
            'status', 'status_reason',
            'fqdn_status', 'website_status',
            'date_last_recon',
            'criticality_score_1',
            'domain', 'asset_class',
            'env_model', 'architectural_model',
            'owners_orig',
            # 'owners_nb', 'owners_group',
            'impacted_group_orig', 'impacted_division_orig',
            'tenant',
            'support_group_website_technical_orig',
            'support_group_website_approvals_orig',
            'is_in_cmdb', 'is_internet_facing', 'is_flagship',
            'is_nonprod_mirror',
            'geo_region_choice', 'geo_region',
            'location_orig', 'location',

            'public_ip_1',
            'ipaddress_public_8',
            'private_ip_1', 'private_ip_2',
            # 'ipaddress_private_8',
            'hostname_orig', 'os_char',
            # 'os_1', 'os_8',
            'software', 'tech_webserver_orig', 'tech_addtl',

            'had_bugbounty', 'is_risky',
            'vuln_scan_coverage', 'date_last_vulnscan',
            'pentest_priority', 'date_last_pentest',
            'site_operation_age',

            'tls_protocol_version', 'certificate',
            'tls_cert_info', 'tls_cert_expires',
            'tls_cert_is_wildcard', 'tls_cert_self_signed', 'tls_cert_sha1',
            'scan_fingerprint_json',
            'cnames', 'dns_a_record_ips',

            'is_cloud_hosted', 'cloud_provider',
            'is_akamai', 'is_load_protected', 'is_waf_protected',

            'feature_acct_mgmt', 'feature_webauth_type',
            'feature_auth_self_registration', 'feature_api',
            'scoping_size', 'scoping_complexity', 'scoping_roles',
            'is_compliance_required',
            'compliance_programs_choice',

            'is_vendor_managed', 'is_vendor_hosted',
            'vendor_company_orig', 'vendor_company_fk',
            'vendor_pocs_orig', 'vendor_url', 'vendor_notes',

            'website_url', 'website_title', 'website_email_orig',
            'website_role',
            'response_code', 'content_length',
            'redirect_health', 'redirect_url',
            'is_vhost', 'is_http2',
            # 'website_homepage_image',
            'risk_analysis_notes',
            'notes',
            'tags',
        )

    # NOTE: This would be for limiting queryset choices down from all to a filtered list of choices
    # -- See netbox/ipam/forms/bulk_import.py -> IPAddressImportForm
    # def __init__(self, data=None, *args, **kwargs):
    #     super().__init__(data, *args, **kwargs)
    #     pass
    #     if data:
            # # Limit business divisions queryset by assigned group
            # # TODO: See line 491 in /dcim/forms/bulk_import.py
            # params = {f"impacted_division_orig__{self.fields['group'].to_field_name}": data.get('impacted_group_orig')}
            # self.fields['impacted_division_orig'].queryset = self.fields['impacted_division_orig'].queryset.filter(**params)

        # Handle poorly formatted redirect URLs
        # def clean_redirect_urls(self):
        #     for val in self.data["redirect_url"]:
                # If redirect_url is a string and not a valid URL, it's probably just a path
                # TODO: For now, changing this field to a CharField until I can add in cleaning

    # NOTE: This is how you clean data on import -- see IPAddressImportForm or
    # for JSON see netbox/utilities/forms/bulk_import.py -> BulkImportForm -> "data" form field
    # def clean(self):
    #     super().clean()

    #     import_method = "JSON"
    #     # Form data or Uploaded File
    #     if self.cleaned_data["scan_fingerprint_json"]

    # def _clean_json(self, data):
    #     """
    #     JSON clean method taken from netbox/utilities/forms/bulk_import.py -> BulkImportForm
    #     """
    #     data = json.loads(data)


class OperatingSystemImportForm(NetBoxModelImportForm):

    class Meta:
        model = OperatingSystem
        fields = (
            'vendor', 'product', 'update',
            'platform_family', 'platform_type',
            'build_number', 'cpe',
        )


class SiteLocationImportForm(NetBoxModelImportForm):
    # -- Choices --
    geo_region_choice = CSVChoiceField(
        choices=GeoRegionChoices,
        required=False,
        help_text=_('Geographic Region from choices'),
    )
    # -- FKs --
    impacted_group_orig = CSVModelChoiceField(
        queryset=BusinessGroup.objects.all(),
        to_field_name="acronym",
        required=False,
        help_text=_('The principal impacted business group for this location')
    )
    impacted_division_orig = CSVModelChoiceField(
        queryset=BusinessDivision.objects.all(),
        to_field_name="acronym",
        required=False,
        help_text=_('The principal impacted business division for this location')
    )

    class Meta:
        model = SiteLocation
        fields = (
            'name', 'slug', 'code',
            'active', 'priority',
            'geo_region_choice',
            'impacted_group_orig', 'impacted_division_orig',
            'timezone_1', 'timezone',
            'street', 'city', 'state', 'country_1',
            'it_infra_contact', 'ranges_tmp1',
            'notes',
        )


class SoftwareImportForm(NetBoxModelImportForm):
    # TODO: Hoping this slug here makes it auto-generate and not have to
    # have slug in the import form -- test this theory.
    slug = SlugField()

    class Meta:
        model = Software
        fields = ('name', 'slug', 'product', 'version', 'raw_banner', 'cpe')


class VendorImportForm(NetBoxModelImportForm):

    class Meta:
        model = Vendor
        fields = (
            'name', 'slug',
            'description',
            'url',
            'vendor_pocs_orig', 'notes',
        )
