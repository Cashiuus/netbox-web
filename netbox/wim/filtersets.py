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
    # 'AggregateFilterSet',
    # 'ASNFilterSet',
    # 'ASNRangeFilterSet',
    # 'IPAddressFilterSet',
    # 'IPRangeFilterSet',
    # 'PrefixFilterSet',
    # 'RoleFilterSet',
    # 'ServiceFilterSet',
    # 'ServiceTemplateFilterSet',
)

class DomainFilterSet(NetBoxModelFilterSet, TenancyFilterSet):
# class DomainFilterSet(NetBoxModelFilterSet):
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

    class Meta:
        model = Domain
        fields = ['id', 'name', 'status']
    
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
        )


class FQDNFilterSet(NetBoxModelFilterSet, TenancyFilterSet):
# class FQDNFilterSet(NetBoxModelFilterSet):
    # -- Model Specific Filters --
    # contains = django_filters.CharFilter(
    #     method='search_contains',
    #     label=_('FQDNs which contain search keyword'),
    # )
    status = django_filters.MultipleChoiceFilter(
        choices=FQDNStatusChoices,
        # null_value=None
    )
    role = django_filters.MultipleChoiceFilter(
        choices=WebsiteRoleChoices
    )

    class Meta:
        model = FQDN
        fields = [
            'id', 'name', 'fqdn_status', 'website_status',
            'public_ip_9', 'ipaddress_public_8', 'owners_9',
        ]
    
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value) |
            Q(ipaddress_public_8__icontains=value) |
            Q(owners_9__icontains=value)
        )
        return queryset.filter(qs_filter)

    def search_contains(self, queryset, name, value):
        value = value.strip()
        if not value:
            return queryset
        try:
            return queryset.filter(fqdn__contains_or_equals=value)

        except (AddrFormatError, ValueError):
            return queryset.none()


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
        fields = ['id', 'vendor', 'product']

