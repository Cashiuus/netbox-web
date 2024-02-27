import django_tables2 as tables
from django_tables2.utils import Accessor
from django.utils.translation import gettext as _

from netbox.tables import NetBoxTable, columns
from tenancy.tables import TenancyColumnsMixin, TenantColumn
from wim.models import *


__all__ = (
    'BusinessGroupTable',
    'BusinessDivisionTable',
    'CertificateTable',
    'OperatingSystemTable',
    'SiteLocationTable',
    'VendorTable',
    'WebEmailTable',
    'SoftwareTable',
)


class CertificateTable(NetBoxTable):
    hash_sha1 = tables.Column(linkify=True)

    fqdn_count = columns.LinkedCountColumn(
        viewname='wim:fqdn_list',
        url_params={'certificate_id': 'pk'},
        verbose_name=_('FQDNs'),
    )

    class Meta(NetBoxTable.Meta):
        model = Certificate
        fields = (
            "hash_sha1", "id",
            "date_issued", "date_expiration",
            "sdn", "scn", "san", "sorg",
            "idn", "icn", "iorg", "signing_algorithm",
            "key_type", "key_bitlength", "is_wildcard", "is_self_signed",
            "hash_sha256", "hash_md5",
            'fqdn_count',
        )
        default_columns = (
            'hash_sha1', 'fqdn_count', 'date_issued', 'date_expiration',
            'scn', 'san', 'sorg'
        )


# class BusinessGroupTable(TenancyColumnsMixin, NetBoxTable):
class BusinessGroupTable(NetBoxTable):
    acronym = tables.Column(
        linkify=True
    )
    fqdn_count = columns.LinkedCountColumn(
        viewname='wim:fqdn_list',
        url_params={'businessgroup_id': 'pk'},
        verbose_name="FQDNs"
    )
    division_count = columns.LinkedCountColumn(
        viewname='wim:businessdivision_list',
        url_params={'businessgroup_id', 'pk'},
        verbose_name="Divisions",
    )

    class Meta(NetBoxTable.Meta):
        model = BusinessGroup
        # exclude = ('id',)
        fields = (
            'pk', 'id',
            'acronym', 'name',
            'fqdn_count',
            'division_count',
        )
        default_columns = ('acronym', 'name', 'fqdn_count')


class BusinessDivisionTable(NetBoxTable):
    acronym = tables.Column(
        linkify=True,
    )

    group = tables.Column(
        accessor=Accessor('group__acronym'),
        linkify=True,
    )

    fqdn_count = columns.LinkedCountColumn(
        viewname='wim:fqdn_list',
        url_params={'businessdivision_id': 'pk'},
        verbose_name="FQDNs",
    )

    class Meta(NetBoxTable.Meta):
        model = BusinessDivision
        # exclude = ('id',)
        fields = (
            'pk', 'id',
            'acronym', 'name', 'group', 'fqdn_count',
        )
        default_columns = ('acronym', 'name', 'group', 'fqdn_count')


# class OperatingSystemTable(TenancyColumnsMixin, NetBoxTable):
class OperatingSystemTable(NetBoxTable):
    # TODO: Fix this so we have a full OS string that is the first column and is linked
    vendor = tables.Column(
        linkify=True,
    )

    # TODO: Check this and add it to fields list once it's working
    fqdn_count = columns.LinkedCountColumn(
        viewname='wim:fqdn_list',
        url_params={'os_1_id': 'pk'},
        verbose_name="FQDNs",
    )
    # status = columns.ChoiceFieldColumn()

    # m2m_field = tables.ManyToManyColumn(
    #     linkify_item=False,
    #     orderable=False,
    #     verbose_name=""
    # )

    color = columns.ColorColumn()

    # notes = columns.MarkdownColumn()
    # tags = columns.TagColumn(
    #     url_name='wim:OperatingSystem_list'
    # )

    class Meta(NetBoxTable.Meta):
        model = OperatingSystem
        # exclude = ('id',)
        fields = (
            'pk', 'id',
            'vendor', 'product', 'update',
            'platform_family', 'platform_type',
            'build_number', 'cpe', 'color',
            'fqdn_count',
            'tags',
        )
        default_columns = (
            'vendor', 'product', 'update', 'fqdn_count', 'platform_type', 'color'
        )


class SiteLocationTable(TenancyColumnsMixin, NetBoxTable):
    code = tables.Column(linkify=True)

    # geo_region_choice = columns.ChoiceFieldColumn(verbose_name="Geo Region")

    # active = columns.BooleanColumn()

    fqdn_count = columns.LinkedCountColumn(
        viewname='wim:fqdn_list',
        url_params={'location_orig_id': 'pk'},
        verbose_name="FQDNs",
    )

    notes = columns.MarkdownColumn()
    tags = columns.TagColumn(url_name='wim:sitelocation_list')

    class Meta(NetBoxTable.Meta):
        model = SiteLocation
        # exclude = ('id',)
        fields = (
            'pk', 'id', 'code', 'name', 'active', 'priority',
            'impacted_group_orig', 'impacted_division_orig',
            'geo_region_choice', 'geo_region', 'tenant',
            'fqdn_count', 'notes', 'tags',
        )
        default_columns = (
            'pk', 'id', 'code', 'name', 'fqdn_count',
            'active', 'priority', 'geo_region_choice',
        )


class SoftwareTable(NetBoxTable):
    name = tables.Column(linkify=True)

    fqdn_count = columns.LinkedCountColumn(
        viewname='wim:fqdn_list',
        url_params={'software_id': 'pk'},
        verbose_name=_('FQDNs'),
    )

    class Meta(NetBoxTable.Meta):
        model = Software
        # exclude = ('id',)
        fields = (
            'name', 'id', 'product', 'version', 'raw_banner',
            'cpe', 'fqdn_count',
        )
        default_columns = ('name', 'product', 'version', 'fqdn_count')


class VendorTable(NetBoxTable):
    name = tables.Column(linkify=True)

    fqdn_count = columns.LinkedCountColumn(
        viewname='wim:fqdn_list',
        url_params={'vendor_id': 'pk'},
        verbose_name=_('FQDNs'),
    )

    tags = columns.TagColumn(
        url_name='wim:vendor_list'
    )

    class Meta(NetBoxTable.Meta):
        model = Vendor
        # exclude = ('id',)
        fields = (
            'pk', 'id', 'name', 'fqdn_count', 'description',
            'vendor_url', 'vendor_pocs_orig', 'notes',
            'slug', 'tags',
        )
        default_columns = ('name', 'fqdn_count', 'vendor_pocs_orig')


class WebEmailTable(NetBoxTable):
    email_address = tables.Column(linkify=True)

    # domain_count = columns.LinkedCountColumn(
    #     viewname='wim:domain_list',
    #     url_params={'webemail_id': 'pk'},
    #     verbose_name=_('Domains'),
    # )

    class Meta(NetBoxTable.Meta):
        model = WebEmail
        # exclude = ('id',)
        fields = (
            'email_address',
        )
        default_columns = ('email_address',)
