import django_tables2 as tables
from django.utils.translation import gettext as _

from wim.models import *
from netbox.tables import NetBoxTable, columns
from tenancy.tables import TenancyColumnsMixin

__all__ = (
    'FQDNTable',
)


class FQDNTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    rir = tables.Column(
        linkify=True
    )
    tags = columns.TagColumn(
        url_name='wim:fqdn_list'
    )
    asn_count = columns.LinkedCountColumn(
        viewname='wim:fqdn_list',
        url_params={'id': 'pk'},
        verbose_name=_('FQDN Count')
    )

    class Meta(NetBoxTable.Meta):
        model = FQDN
        fields = (
            'pk', 'name', 'description', 'owners', 'business_group', 'business_division',
        )
        default_columns = ('pk', 'name')


