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
from utilities.forms.fields import (
    CSVChoiceField, CSVContentTypeField, CSVModelChoiceField, CSVModelMultipleChoiceField, CSVTypedChoiceField,
    SlugField,
)

__all__ = (
    'DomainImportForm',
    'FQDNImportForm',
    'BusinessGroupImportForm',
    'BusinessDivisionImportForm',
    'OperatingSystemImportForm',
    'SiteLocationImportForm',
    'VendorImportForm',
    'WebserverFrameworkImportForm',
)


class DomainImportForm(NetBoxModelImportForm):
    # -- Choices Fields --
    status = CSVChoiceField(
        choices=DomainStatusChoices,
        help_text=_('Domain root operational status')
    )
    asset_confidence = CSVChoiceField(
        choices=AssetConfidenceChoices,
        required=False,
        help_text=_('Domain attribution confidence level')
    )
    ownership_type = CSVChoiceField(
        choices=DomainOwnershipStatusChoices,
        required=False,
        help_text=_('Ownership type for this domain')
    )
    # -- FKs --
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Assigned tenant')
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
        fields = [
            'name', 'status', 'asset_confidence', 'ownership_type',
            'meets_standards',
            'tenant',
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
        ]



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
    tls_protocol_version = CSVChoiceField(
        choices=TransportLayerSecurityVersionChoices,
        required=False,
        help_text=_('The TLS/SSL protocol version running on this property, if applicable')
    )
    redirect_health = CSVChoiceField(
        choices=RedirectStatusChoices,
        required=False,
        help_text=_('The health status of redirect config, if this property is setup as a redirect')
    )
    feature_webauth_type = CSVChoiceField(
        choices=WebAuthChoices,
        required=False,
        help_text=_('Type of auth method employed by the website, if applicable')
    )

    # -- Numbers Fields --
    criticality_score_1 = forms.IntegerField(
    #     min_value=1,
    #     max_value=100,
        required=False,
        help_text=_('Asset criticality score for prioritization (1=low, 100=critical)')
    )
    scoping_size = forms.IntegerField(required=False)
    scoping_complexity = forms.IntegerField(required=False)
    scoping_roles = forms.IntegerField(required=False)

    # -- Bools --
    mark_triaging = forms.BooleanField(
        required=False,
        help_text=_('Is the asset marked for triaging focus currently'),
    )

    # -- FK Fields --
    domain = CSVModelChoiceField(
        queryset=Domain.objects.all(),
        to_field_name='name',
        required=False,
        help_text=_('Parent domain for this asset')
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
        help_text=_('Assigned site location code')
    )
    location = CSVModelChoiceField(
        queryset=Site.objects.all(),
        # TODO: I may want to re-do how I did this, and import all sites
        # so that the acronym is in the "name" field...
        to_field_name="facility",
        required=False,
        help_text=_('Assigned tenancy site code')
    )
    ipaddress_public_8 = CSVModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        to_field_name='address',
        help_text=_('Public IP address linked to IPAM')
    )
    ipaddress_private_8 = CSVModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        to_field_name='address',
        help_text=_('Private IP address linked to IPAM')
    )
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Assigned tenant')
    )

    # -- M2M Fields --
    # compliance_programs = 

    class Meta:
        model = FQDN
        # exclude = ('id',)
        # import_id_fields = ['name',]      # This doesn't exist. I'll have to build it.
        fields = (
            "name", "mark_triaging", "asset_confidence",
            'status', 'status_reason', 
            'fqdn_status', 'website_status', 'website_role',
            'domain', 'asset_class',
            'env_model', 'architectural_model',
            'owners_orig',
            # 'owners_nb', 'owners_group',
            'impacted_group_orig', 'impacted_division_orig',
            'tenant',
            'support_group_website_technical_orig',
            'support_group_website_approvals_orig',
            'is_in_cmdb', 'is_internet_facing', 'is_flagship',
            'location_orig', 'geo_region_choice',
            'location', 'geo_region',
            'public_ip_1', 'ipaddress_public_8',
            'private_ip_1', 'private_ip_2',
            # 'ipaddress_private_8',
            'hostname_orig', 'os_char',
            # 'os_1', 'os_8',
            'tech_webserver_orig', 'tech_addtl',
            # 'tech_webserver_1',
            'criticality_score_1',
            'cnames', 'dns_a_record_ips',
            'tls_cert_info', 'tls_cert_expires', 'tls_cert_sha1',
            'tls_cert_is_wildcard', 'tls_protocol_version',
            'is_vhost', 'is_http2',
            'response_code', 'content_length',
            'redirect_health', 'redirect_url',
            # TODO: Clean this up later on
            # 'parked_status',
            'is_cloud_hosted', 'cloud_provider',
            'is_akamai', 'is_load_protected', 'is_waf_protected',
            'had_bugbounty', 'is_risky', 'vuln_assessment_priority',
            'last_vuln_assessment', 'vuln_scan_coverage', 'vuln_scan_last_date',
            'feature_acct_mgmt', 'feature_webauth_type',
            'feature_auth_self_registration', 'feature_api',
            'scoping_size', 'scoping_complexity', 'scoping_roles',
            'is_compliance_required', 
            # 'compliance_programs',
            'is_vendor_managed', 'is_vendor_hosted', 
            'vendor_company_orig', 'vendor_pocs_orig',
            'vendor_url', 'vendor_notes',

            'website_url', 'website_title', 'website_email_orig',
            'website_role',
            'site_operation_age',

            'website_homepage_image',
            'notes',
            'risk_analysis_notes',
            'tags',
        )
    
    # def __init__(self, data=None, *args, **kwargs):
    #     super().__init__(data, *args, **kwargs)
    #     pass
        # if data:
            # # Limit business divisions queryset by assigned group
            # # TODO: See line 491 in /dcim/forms/bulk_import.py
            # params = {f"impacted_division_orig__{self.fields['group'].to_field_name}": data.get('impacted_group_orig')}
            # self.fields['impacted_division_orig'].queryset = self.fields['impacted_division_orig'].queryset.filter(**params)

        # Handle poorly formatted redirect URLs
        # def clean_redirect_urls(self):
        #     for val in self.data["redirect_url"]:
                # If redirect_url is a string and not a valid URL, it's probably just a path
                # TODO: For now, changing this field to a CharField until I can add in cleaning




class BusinessGroupImportForm(NetBoxModelImportForm):
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


class BusinessDivisionImportForm(NetBoxModelImportForm):

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


class OperatingSystemImportForm(NetBoxModelImportForm):

    class Meta:
        model = OperatingSystem
        fields = (
            'vendor', 'product', 'update',
            'platform_family', 'platform_type',
            'build_number', 'cpe',
        )


class SiteLocationImportForm(NetBoxModelImportForm):
    # Testing to import my original choices, which are done differently
    # geo_region_orig = Field(attribute="get_geo_region_display")

    geo_region_choice = CSVChoiceField(
        choices=GeoRegionChoices,
        help_text=_('Geographic Region from choices')
    )

    class Meta:
        model = SiteLocation
        fields = (
            'name', 'slug', 'code', 'geo_region_choice',
            # 'impacted_group_orig', 'impacted_division_orig',
            'priority', 'street', 'city', 'state', 'country_1', 
            'timezone_1', 'timezone', 'it_infra_contact', 'ranges_tmp1', 
            'notes'
        )


class VendorImportForm(NetBoxModelImportForm):

    class Meta:
        model = Vendor
        fields = ('name',)


class WebserverFrameworkImportForm(NetBoxModelImportForm):

    class Meta:
        model = WebserverFramework
        fields = ('name', 'product', 'version', 'raw_banner', 'cpe')


