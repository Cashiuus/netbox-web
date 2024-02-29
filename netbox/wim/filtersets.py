import django_filters
import netaddr
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext as _
from netaddr.core import AddrFormatError

from dcim.models import Device, Region, Site
from ipam.models import IPAddress
from netbox.filtersets import (
    ChangeLoggedModelFilterSet, OrganizationalModelFilterSet, NetBoxModelFilterSet
)
from tenancy.filtersets import TenancyFilterSet
from utilities.filters import (
    ContentTypeFilter, MultiValueCharFilter,
    MultiValueNumberFilter, NumericArrayFilter,
    TreeNodeMultipleChoiceFilter,
)
# from virtualization.models import VirtualMachine, VMInterface
from .choices import *
from .models import *


__all__ = (
    'BrandFilterSet',
    'CertificateFilterSet',
    'DomainFilterSet',
    'FQDNFilterSet',
    'BusinessGroupFilterSet',
    'BusinessDivisionFilterSet',
    'OperatingSystemFilterSet',
    'SiteLocationFilterSet',
    'SoftwareFilterSet',
    'VendorFilterSet',
    'WebEmailFilterSet',
)





class CertificateFilterSet(NetBoxModelFilterSet):
    # -- Char Fields --
    sdn = MultiValueCharFilter(
        lookup_expr="icontains",
        label=_('Subject DN')
    )
    scn = MultiValueCharFilter(
        lookup_expr="icontains",
        label=_('Subject CN')
    )
    san = MultiValueCharFilter(
        lookup_expr="icontains",
        label=_('Subject AN')
    )
    # -- Multiple Choice Fields --
    # signing_algorithm = django_filters.MultipleChoiceFilter(
    #     choices=CertSigningAlgorithmChoices,
    #     # null_value=None
    # )
    key_bitlength = django_filters.MultipleChoiceFilter(
        choices=CertBitLengthChoices,
        # null_value=None
    )

    # -- Dates --
    date_expiration = django_filters.DateFilter()
    date_expiration__before = django_filters.DateFilter(
        field_name='date_expiration',
        lookup_expr='lte',
        label=_('Expiring Before'),
    )

    class Meta:
        model = Certificate
        fields = [
            'id', 'hash_sha1', 'san', 'scn', 'sdn',
            'key_bitlength',
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(hash_sha1__icontains=value) |
            Q(san__icontains=value)
        )


class DomainFilterSet(NetBoxModelFilterSet, TenancyFilterSet):
    # -- Char Fields --
    name = MultiValueCharFilter(
        lookup_expr="icontains",
        label=_('Name')
    )

    # TODO: Need to add the method this references - search_contains()
    # contains = django_filters.CharFilter(
    #     method='search_contains',
    #     label=_('Domains which contain this prefix or IP'),
    # )

    # -- Multiple Choice Fields --
    status = django_filters.MultipleChoiceFilter(
        choices=DomainStatusChoices,
        # null_value=None
    )
    asset_confidence = django_filters.MultipleChoiceFilter(
        choices=AssetConfidenceChoices,
        # null_value=None
    )
    ownership_type = django_filters.MultipleChoiceFilter(
        choices=DomainOwnershipStatusChoices,
        label=_('Ownership'),
    )

    # -- FKs --
    brand_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Brand.objects.all(),
        field_name='brand',
        label=_('Brand/Acquisition'),
    )
    # -- Dates --
    date_last_recon_scanned = django_filters.DateFilter()
    date_last_recon_scanned__before = django_filters.DateFilter(
        field_name='date_last_recon_scanned',
        lookup_expr='lte',
        label=_('Last Scanned Before'),
    )
    date_registrar_expiry = django_filters.DateFilter()
    date_registrar_expiry__before = django_filters.DateFilter(
        field_name='date_registrar_expiry',
        lookup_expr='lte',
        label=_('Expired Before'),
    )

    class Meta:
        model = Domain
        fields = [
            'id', 'name', 'status', 'asset_confidence',
            'brand_id', 'meets_standards',
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
        )


class FQDNFilterSet(NetBoxModelFilterSet, TenancyFilterSet):
    # -- Char --
    name = MultiValueCharFilter(
        lookup_expr="icontains"
    )
    # -- Choices --
    status = django_filters.MultipleChoiceFilter(
        choices=FQDNStatusChoices,
        # null_value=None
    )
    asset_class = django_filters.MultipleChoiceFilter(
        choices=AssetClassChoices,
    )
    asset_confidence = django_filters.MultipleChoiceFilter(
        choices=AssetConfidenceChoices,
    )
    fqdn_status = django_filters.MultipleChoiceFilter(
        choices=FQDNOpsStatusChoices,
    )
    website_status = django_filters.MultipleChoiceFilter(
        choices=WebsiteOpsStatusChoices,
    )
    geo_region_choice = django_filters.MultipleChoiceFilter(
        choices=GeoRegionChoices,
    )
    compliance_programs_choice = django_filters.MultipleChoiceFilter(
        choices=ComplianceProgramChoices,
    )
    tls_protocol_version = django_filters.MultipleChoiceFilter(
        choices=TransportLayerSecurityVersionChoices,
    )

    # -- Booleans --
    is_risky = django_filters.BooleanFilter(label=_('Is Risky'))
    had_bugbounty = django_filters.BooleanFilter(label=_('Had Bug Bounty Submission'))
    vuln_scan_coverage = django_filters.BooleanFilter(label=_('Vuln Scanner Coverage'))
    is_in_cmdb = django_filters.BooleanFilter(
        label=_('Is In CMDB?'),
    )
    is_nonprod_mirror = django_filters.BooleanFilter(
        label=_('Is Nonprod Mirror'),
    )
    tls_cert_self_signed = django_filters.BooleanFilter(label=_('TLS Cert Is Self-Signed'))
    is_vendor_managed = django_filters.BooleanFilter(label=_('Vendor Managed'))

    # -- Dates --
    tls_cert_expires = django_filters.DateFilter()
    tls_cert_expires__before = django_filters.DateFilter(
        field_name='tls_cert_expires',
        lookup_expr='lte',
        label=_('TLS Cert Expires Before'),
    )
    date_last_recon = django_filters.DateFilter()
    date_last_recon__before = django_filters.DateFilter(
        field_name='date_last_recon',
        lookup_expr='lte',
        label=_('Last Recon Before'),
    )

    # -- FKs --
    # -- Related Objects Handlers/Filters --
    domain_id = django_filters.ModelMultipleChoiceFilter(
        field_name='domain',
        queryset=Domain.objects.all(),
        label=_('Domain (ID)'),
    )
    # NOTE: I chose single choice on form, so doing single choice filter here too
    certificate = django_filters.ModelChoiceFilter(
        queryset=Certificate.objects.all(),
        label=_('TLS Certificate'),
    )
    certificate_id = django_filters.ModelChoiceFilter(
        queryset=Certificate.objects.all(),
        label=_('TLS Certificate (ID)'),
    )
    impacted_group_orig = django_filters.ModelMultipleChoiceFilter(
        queryset=BusinessGroup.objects.all(),
        label=_('Business Group')
    )
    businessgroup_id = django_filters.ModelMultipleChoiceFilter(
        field_name='impacted_group_orig',
        queryset=BusinessGroup.objects.all(),
        label=_('Org Group (ID)'),
    )
    impacted_division_orig = django_filters.ModelMultipleChoiceFilter(
        queryset=BusinessDivision.objects.all(),
        label=_('Business Division'),
    )
    businessdivision_id = django_filters.ModelMultipleChoiceFilter(
        field_name='impacted_division_orig',
        queryset=BusinessDivision.objects.all(),
        label=_('Org Division (ID)'),
    )
    location_orig = django_filters.ModelMultipleChoiceFilter(
        queryset=SiteLocation.objects.all(),
        label=_('Location (Orig)'),
    )
    location_orig_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SiteLocation.objects.all(),
        field_name='location_orig',
        label=_('Location (Orig-ID)'),
    )
    location = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        label=_('Location (NB)')
    )
    location_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        field_name='location',
        label=_('Location (NB-ID)'),
    )
    # NOTE: dcim/filtersets.py uses a TreeNodeMultipleChoiceFilter for Region field
    geo_region = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(),
        label=_('Region (NB)'),
    )
    geo_region_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(),
        field_name="geo_region",
        label=_('Region (NB-ID)'),
    )
    ipaddress_public_8_id = django_filters.ModelMultipleChoiceFilter(
        field_name='ipaddress_public_8',
        queryset=IPAddress.objects.all(),
        label=_('Public IP (ID)'),
    )

    # -- Vendor FK + Serializer --
    vendor_company_fk = django_filters.ModelMultipleChoiceFilter(
        field_name='vendor_company_fk__slug',
        queryset=Vendor.objects.all(),
        to_field_name='slug',
        label=_('Vendor (slug)'),
    )
    vendor_id = django_filters.ModelMultipleChoiceFilter(
        field_name='vendor_company_fk',
        queryset=Vendor.objects.all(),
        label=_('Vendor (ID)'),
    )
    # -- Software M2M + Serializer --
    software = django_filters.ModelMultipleChoiceFilter(
        # TODO: Which field should I use here, name or slug?
        field_name='software__name',
        queryset=Software.objects.all(),
        to_field_name='software',
        label=_('Software')
    )
    software_id = django_filters.ModelMultipleChoiceFilter(
        field_name='software',
        queryset=Software.objects.all(),
        label=_('Software (ID)')
    )

    class Meta:
        model = FQDN
        fields = [
            'id', 'name', 'slug',
            'status', 'mark_triaging', 'asset_confidence',
            'asset_class',
            'fqdn_status', 'website_status',
            'is_flagship', 'is_nonprod_mirror',
            'is_in_cmdb',
            'owners_orig',
            'public_ip_1', 'ipaddress_public_8',
            # 'date_last_recon',
            'vuln_scan_coverage', 'date_last_vulnscan',
            'compliance_programs_choice',
            # 'is_vendor_managed',
        ]

    # NOTE: This search controls the "quick search" in the tab of the listview table
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(public_ip_1__icontains=value) |
            Q(ipaddress_public_8__address__startswith=value) |
            Q(owners_orig__icontains=value)
            # Q(software__icontains=value )
        )

    # def search_contains(self, queryset, name, value):
    #     value = value.strip()
    #     if not value:
    #         return queryset
    #     try:
    #         return queryset.filter(fqdn__contains_or_equals=value)

    #     except (AddrFormatError, ValueError):
    #         return queryset.none()


#
# -- Secondary Sets
#

class BrandFilterSet(OrganizationalModelFilterSet):

    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug']


# class BusinessGroupFilterSet(OrganizationalModelFilterSet, TenancyFilterSet):
class BusinessGroupFilterSet(OrganizationalModelFilterSet):

    class Meta:
        model = BusinessGroup
        fields = ['id', 'name', 'slug', 'acronym']


class BusinessDivisionFilterSet(OrganizationalModelFilterSet):

    class Meta:
        model = BusinessDivision
        fields = ['id', 'name', 'slug', 'acronym']


class OperatingSystemFilterSet(OrganizationalModelFilterSet):

    class Meta:
        model = OperatingSystem
        fields = (
            'id', 'name', 'slug', 'vendor', 'product', 'update',
            'platform_family', 'platform_type',
            'build_number', 'cpe', 'color',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(product__icontains=value)
        )


class SiteLocationFilterSet(OrganizationalModelFilterSet):

    class Meta:
        model = SiteLocation
        fields = (
            'id', 'name', 'slug', 'code',
            'impacted_group_orig', 'impacted_division_orig',
            'geo_region_choice',
            'geo_region', 'tenant',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(code__icontains=value)
        )


class SoftwareFilterSet(OrganizationalModelFilterSet):

    name = MultiValueCharFilter(
        lookup_expr="icontains"
    )
    product = MultiValueCharFilter(
        lookup_expr="icontains"
    )

    class Meta:
        model = Software
        fields = (
            'id', 'name', 'slug',
            'product', 'version', 'raw_banner', 'cpe',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(product__icontains=value)
        )


class VendorFilterSet(OrganizationalModelFilterSet):

    class Meta:
        model = Vendor
        fields = (
            'id', 'name', 'slug',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
        )


class WebEmailFilterSet(OrganizationalModelFilterSet):

    class Meta:
        model = WebEmail
        fields = (
            'id', 'name', 'slug', 'email_address', 'domain',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(email_address__icontains=value)
        )
