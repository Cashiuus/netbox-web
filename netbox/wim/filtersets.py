import django_filters
import netaddr
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext as _
from netaddr.core import AddrFormatError

from dcim.models import Device, Region, Site
from netbox.filtersets import ChangeLoggedModelFilterSet, OrganizationalModelFilterSet, NetBoxModelFilterSet
from tenancy.filtersets import TenancyFilterSet
from utilities.filters import (
    ContentTypeFilter, MultiValueCharFilter, MultiValueNumberFilter, NumericArrayFilter, TreeNodeMultipleChoiceFilter,
)
# from virtualization.models import VirtualMachine, VMInterface
from .choices import *
from .models import *


__all__ = (
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

    date_last_recon_canned = django_filters.DateFilter()
    scanned_before = django_filters.DateFilter(
        field_name='date_last_recon_scanned',
        lookup_expr='lte'
    )

    class Meta:
        model = Domain
        fields = [
            'id', 'name', 'status', 'asset_confidence',
            'date_registrar_expiry', 'date_last_recon_scanned',
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
    fqdn_status = django_filters.MultipleChoiceFilter(
        choices=FQDNOpsStatusChoices,
    )
    website_status = django_filters.MultipleChoiceFilter(
        choices=WebsiteOpsStatusChoices,
    )
    geo_region_choice = django_filters.MultipleChoiceFilter(
        choices=GeoRegionChoices,
        # required=False,
    )
    compliance_programs_choice = django_filters.MultipleChoiceFilter(
        choices=ComplianceProgramChoices,
    )
    # website_role = django_filters.MultipleChoiceFilter(
    #     choices=WebsiteRoleChoices
    # )

    # -- FKs --
    impacted_group_orig = django_filters.ModelMultipleChoiceFilter(
        queryset=BusinessGroup.objects.all(),
        label=_('Business Group')
    )
    impacted_division_orig = django_filters.ModelMultipleChoiceFilter(
        queryset=BusinessDivision.objects.all(),
        label=_('Business Division')
    )
    geo_region = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(),
        label=_('Geographic region linked to org model'),
    )

    class Meta:
        model = FQDN
        fields = [
            'id', 'name', 
            'status', 'mark_triaging', 'asset_confidence',
            'fqdn_status', 'website_status',
            'asset_class',
            'impacted_group_orig', 'impacted_division_orig',
            'geo_region_choice', 'geo_region',
            'owners_orig',
            'public_ip_1', 'ipaddress_public_8',
            'compliance_programs_choice',
        ]
    
    # NOTE: This search controls the "quick search" in the tab of the listview table
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        # qs_filter = (
        #     Q(name__icontains=value) |
        #     Q(public_ip_1__icontains=value) |
        #     Q(ipaddress_public_8__icontains=value) |
        #     Q(owners_orig__icontains=value)
        # )
        # return queryset.filter(qs_filter)
        return queryset.filter(
            Q(name__icontains=value)
        )

    # def search_contains(self, queryset, name, value):
    #     value = value.strip()
    #     if not value:
    #         return queryset
    #     try:
    #         return queryset.filter(fqdn__contains_or_equals=value)

    #     except (AddrFormatError, ValueError):
    #         return queryset.none()


# class BusinessGroupFilterSet(OrganizationalModelFilterSet, TenancyFilterSet):
class BusinessGroupFilterSet(OrganizationalModelFilterSet):

    class Meta:
        model = BusinessGroup
        fields = ['id', 'name', 'acronym']


class BusinessDivisionFilterSet(OrganizationalModelFilterSet):

    class Meta:
        model = BusinessDivision
        fields = ['id', 'name', 'acronym']


class OperatingSystemFilterSet(OrganizationalModelFilterSet):

    class Meta:
        model = OperatingSystem
        fields = (
            'id', 'vendor', 'product', 'update',
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
            'name',
        )



class WebEmailFilterSet(OrganizationalModelFilterSet):

    class Meta:
        model = WebEmail
        fields = (
            'email_address', 'domain_tmp',
        )


class WebserverFrameworkFilterSet(OrganizationalModelFilterSet):

    class Meta:
        model = WebserverFramework
        fields = (
            'name', 'product', 'version', 'raw_banner', 'cpe',
        )
    
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(raw_banner__icontains=value)
        )

