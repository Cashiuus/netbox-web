import django_tables2 as tables
from django.utils.translation import gettext as _

from wim.models import *
from netbox.tables import NetBoxTable, columns
from tenancy.tables import TenancyColumnsMixin




class DomainTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.Column(
        linkify=True
    )

    # site_count = columns.LinkedCountColumn(
    #     viewname='dcim:site_list',
    #     url_params={'asn_id': 'pk'},
    #     verbose_name=_('Site Count')
    # )
    # provider_count = columns.LinkedCountColumn(
    #     viewname='circuits:provider_list',
    #     url_params={'asn_id': 'pk'},
    #     verbose_name=_('Provider Count')
    # )
    # sites = columns.ManyToManyColumn(
    #     linkify_item=True
    # )
    # comments = columns.MarkdownColumn()
    # tags = columns.TagColumn(
    #     url_name='ipam:asn_list'
    # )

    class Meta(NetBoxTable.Meta):
        model = Domain
        fields = (
            'pk', 'name',
        )
        default_columns = (
            'pk', 'name',
        )
