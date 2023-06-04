import django_tables2 as tables
from django_tables2.utils import Accessor
from django.utils.translation import gettext as _

from netbox.tables import NetBoxTable, columns
from tenancy.tables import TenancyColumnsMixin, TenantColumn
from wim.models import *


__all__ = (
    'BusinessGroupTable',
    'BusinessDivisionTable',
    'OperatingSystemTable',
    'SiteLocationTable',
    'VendorTable',
    'WebserverFrameworkTable',
)


# class BusinessGroupTable(TenancyColumnsMixin, NetBoxTable):
class BusinessGroupTable(NetBoxTable):
    acronym = tables.Column(
        linkify=True
    )

    # TODO: This isn't working, only getting 0 counts for all rows
    division_count = columns.LinkedCountColumn(
        viewname='wim:businessdivision_list',
        url_params={'id', 'pk'},
        verbose_name="Divisions"
    )

    # notes = columns.MarkdownColumn()
    # tags = columns.TagColumn(
    #     url_name='wim:BusinessGroup_list'
    # )

    class Meta(NetBoxTable.Meta):
        model = BusinessGroup
        exclude = ('id',)
        fields = (
            'acronym', 'name',
        )
        default_columns = ('acronym', 'name')


class BusinessDivisionTable(NetBoxTable):
    acronym = tables.Column(
        linkify=True
    )

    group = tables.Column(
        accessor=Accessor('group__acronym'),
        linkify=True,
    )
    # TODO: Did these counts based on Devices tables, but it's not working
    fqdn_count = columns.LinkedCountColumn(
        viewname='wim:fqdn_list',
        url_params={'fqdn_id': 'pk'},
        verbose_name="FQDNs"
    )

    # notes = columns.MarkdownColumn()
    # tags = columns.TagColumn(
    #     url_name='wim:BusinessDivision_list'
    # )

    class Meta(NetBoxTable.Meta):
        model = BusinessDivision
        exclude = ('id',)
        fields = (
            'acronym', 'name', 'group', 'fqdn_count',
        )
        default_columns = ('acronym', 'name', 'group')



# class OperatingSystemTable(TenancyColumnsMixin, NetBoxTable):
class OperatingSystemTable(NetBoxTable):
    # TODO: Fix this so we have a full OS string that is the first column and is linked
    vendor = tables.Column(
        linkify=True
    )

    # TODO: Check this and add it to fields list once it's working
    fqdn_count = columns.LinkedCountColumn(
        viewname='wim:fqdn_list',
        url_params={'os_1_id', 'pk'},
        verbose_name="FQDNs"
    )
    # status = columns.ChoiceFieldColumn()

    # is_ = columns.BooleanColumn(verbose_name="")

    # m2m_field = tables.ManyToManyColumn(
    #     linkify_item=False,
    #     orderable=False,
    #     verbose_name=""
    # )

    # notes = columns.MarkdownColumn()
    # tags = columns.TagColumn(
    #     url_name='wim:OperatingSystem_list'
    # )

    class Meta(NetBoxTable.Meta):
        model = OperatingSystem
        exclude = ('id',)
        fields = ('vendor', 'product', 'update', 'build', 'family', 'cpe', 'fqdn_count')
        default_columns = ('vendor', 'product', 'update', 'family', 'build')


class SiteLocationTable(TenancyColumnsMixin, NetBoxTable):
    code = tables.Column(linkify=True)

    geo_region_choice = columns.ChoiceFieldColumn(verbose_name="Geo Region")

    # TODO: This is how we'll link to the NetBox way of doing geo regions
    # However, this links through the "site" object, so may not be able to do that in here
    # May just need to do that straight from assets that are assigned once I do the NetBox way of 'sites'

    # geo_region = tables.Column(
    #     accessor=Accessor('site__region'),
    #     linkify=True,
    # )

    # TODO: Doesn't work
    fqdn_count = columns.LinkedCountColumn(
        viewname='wim:fqdn_list',
        url_params={'location_orig_id', 'pk'},
        verbose_name="FQDNs"
    )

    notes = columns.MarkdownColumn()
    tags = columns.TagColumn(
        url_name='wim:sitelocation_list'
    )

    class Meta(NetBoxTable.Meta):
        model = SiteLocation
        exclude = ('id',)
        fields = (
            'code', 'name', 'priority',
            'impacted_group_orig', 'impacted_division_orig',
            'geo_region_choice', 'geo_region', 'tenant',
            'fqdn_count', 'notes', 'tags',
        )
        default_columns = ('code', 'name', 'priority', 'geo_region_choice')


class VendorTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = Vendor
        exclude = ('id',)
        fields = (
            'name',
        )
        default_columns = ('name',)


class WebserverFrameworkTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = WebserverFramework
        exclude = ('id',)
        fields = (
            'name', 'product', 'version', 'raw_banner', 'cpe',
        )
        default_columns = ('name', 'raw_banner', 'cpe', 'product', 'version')