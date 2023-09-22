import django_filters
import netaddr
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext as _
from netaddr.core import AddrFormatError

from dcim.models import Device, Region, Site
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
    'DomainFilterSet',
    'FQDNFilterSet',
    'BusinessGroupFilterSet',
    'BusinessDivisionFilterSet',
    'OperatingSystemFilterSet',
    'SiteLocationFilterSet',
    'VendorFilterSet',
    'WebEmailFilterSet',
    'WebserverFrameworkFilterSet',
)


class DomainFilterSet(NetBoxModelFilterSet, TenancyFilterSet):
    # TODO: Need to add the method this references - search_contains()
    # contains = django_filters.CharFilter(
    #     method='search_contains',
    #     label=_('Domains which contain this prefix or IP'),
    # )
    # -- Multiple Choice Fields
    status = django_filters.MultipleChoiceFilter(
        choices=DomainStatusChoices,
        # null_value=None
    )
    asset_confidence = django_filters.MultipleChoiceFilter(
        choices=AssetConfidenceChoices,
        # null_value=None
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
            'brand_id',
            # 'date_registrar_expiry', 'date_last_recon_scanned',
            'meets_standards',
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
        )




class FQDNFilterSet(NetBoxModelFilterSet, TenancyFilterSet):

    # -- Model Specific Filters --
    # contains = django_filters.CharFilter(
    #     method='search_contains',
    #     label=_('FQDNs which contain search keyword'),
    # )

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
    # website_role = django_filters.MultipleChoiceFilter(
    #     choices=WebsiteRoleChoices
    # )

    # -- FKs --
    # brand = django_filters.ModelMultipleChoiceFilter(
    #     queryset=Brand.objects.all(),
    #     label=_('Brand/Acquisition')
    # )
    impacted_group_orig = django_filters.ModelMultipleChoiceFilter(
        queryset=BusinessGroup.objects.all(),
        label=_('Business Group')
    )
    impacted_division_orig = django_filters.ModelMultipleChoiceFilter(
        queryset=BusinessDivision.objects.all(),
        label=_('Business Division')
    )
    location_orig = django_filters.ModelMultipleChoiceFilter(
        queryset=SiteLocation.objects.all(),
        label=_('Location (Orig)')
    )
    location = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        label=_('Location (NB)')
    )
    # NOTE: dcim/filtersets.py uses a TreeNodeMultipleChoiceFilter for Region field
    geo_region = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(),
        label=_('Region (NB)'),
    )
    # vendor_company_fk = django_filters.ModelMultipleChoiceFilter(
    #     queryset=Vendor.objects.all(),
    #     label=_('Vendor Company (FK)'),
    # )

    # -- Booleans --
    is_in_cmdb = django_filters.BooleanFilter(
        label=_('Is In CMDB?'),
    )
    # is_nonprod_mirror = django_filters.BooleanFilter(
    #     label=_('Is Nonprod Mirror'),
    # )

    # -- Related Objects Handlers/Filters --
    domain_id = django_filters.ModelMultipleChoiceFilter(
        field_name='domain',
        queryset=Domain.objects.all(),
        label=_('Domain (ID)'),
    )
    businessgroup_id = django_filters.ModelMultipleChoiceFilter(
        field_name='impacted_group_orig',
        queryset=BusinessGroup.objects.all(),
        label=_('Org Group (ID)'),
    )
    businessdivision_id = django_filters.ModelMultipleChoiceFilter(
        field_name='impacted_division_orig',
        queryset=BusinessDivision.objects.all(),
        label=_('Org Division (ID)'),
    )
    webserverframework_id = django_filters.ModelMultipleChoiceFilter(
        field_name='tech_webserver_1',
        queryset=WebserverFramework.objects.all(),
        label=_('Web Framework (ID)'),
    )
    vendor_id = django_filters.ModelMultipleChoiceFilter(
        field_name='vendor_company_fk',
        queryset=Vendor.objects.all(),
        label=_('Vendor (ID)'),
    )
    vendor_company_fk = django_filters.ModelMultipleChoiceFilter(
        field_name='vendor_company_fk__slug',
        queryset=Vendor.objects.all(),
        to_field_name='slug',
        label=_('Vendor (slug)'),
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
            'impacted_group_orig', 'impacted_division_orig',
            'geo_region_choice', 'geo_region',
            'location_orig', 'location',
            'owners_orig',
            'public_ip_1', 'ipaddress_public_8',
            'date_last_recon',
            'vuln_scan_coverage', 'date_last_vulnscan',
            'compliance_programs_choice',
            'is_vendor_managed',
        ]

    # NOTE: This search controls the "quick search" in the tab of the listview table
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        return queryset.filter(
            Q(name__icontains=value) |
            Q(public_ip_1__icontains=value)
        )

    # def search_contains(self, queryset, name, value):
    #     value = value.strip()
    #     if not value:
    #         return queryset
    #     try:
    #         return queryset.filter(fqdn__contains_or_equals=value)

    #     except (AddrFormatError, ValueError):
    #         return queryset.none()


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
            'id', 'name', 'slug', 'email_address', 'domain_tmp',
        )


class WebserverFrameworkFilterSet(OrganizationalModelFilterSet):

    class Meta:
        model = WebserverFramework
        fields = (
            'id', 'name', 'slug', 'product', 'version', 'raw_banner', 'cpe',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(raw_banner__icontains=value)
        )

