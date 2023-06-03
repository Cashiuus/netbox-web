import django_tables2 as tables
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


class BusinessGroupTable(TenancyColumnsMixin, NetBoxTable):
    # notes = columns.MarkdownColumn()
    # tags = columns.TagColumn(
    #     url_name='wim:BusinessGroup_list'
    # )

    class Meta:
        model = BusinessGroup
        exclude = ('id',)
        fields = (
            'name', 'acronym', '',
        )
        default_columns = ('name', 'acronym')


class BusinessDivisionTable(TenancyColumnsMixin, NetBoxTable):
    # notes = columns.MarkdownColumn()
    # tags = columns.TagColumn(
    #     url_name='wim:BusinessDivision_list'
    # )

    class Meta:
        model = BusinessDivision
        exclude = ('id',)
        fields = (
            'name', 'acronym', 'group', 'description'
        )
        default_columns = ('name', 'acronym', 'group')



class OperatingSystemTable(TenancyColumnsMixin, NetBoxTable):
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

    class Meta:
        model = OperatingSystem
        exclude = ('id',)
        fields = ('vendor', 'product', 'update', 'build', 'family', 'cpe',)
        default_columns = ('vendor', 'product', 'update', 'family', 'build')


class SiteLocationTable(TenancyColumnsMixin, NetBoxTable):
    # notes = columns.MarkdownColumn()
    # tags = columns.TagColumn(
    #     url_name='wim:BusinessDivision_list'
    # )

    class Meta:
        model = SiteLocation
        exclude = ('id',)
        fields = (
            'name', 'code', 
            'impacted_group_orig', 'impacted_division_orig',
            'geo_region_choice',
            'geo_region', 'tenant',
        )
        default_columns = ('name', 'code', 'geo_region_choice')


class VendorTable(NetBoxTable):

    class Meta:
        model = Vendor
        exclude = ('id',)
        fields = (
            'name',
        )


class WebserverFrameworkTable(NetBoxTable):

    class Meta:
        model = WebserverFramework
        exclude = ('id',)
        fields = (
            'name', 'product', 'version', 'raw_banner', 'cpe',
        )