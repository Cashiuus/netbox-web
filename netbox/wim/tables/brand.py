import django_tables2 as tables
from django_tables2.utils import Accessor
from django.utils.translation import gettext as _

from netbox.tables import NetBoxTable, columns
from wim.models import *


__all__ = (
    'BrandTable',
)


class BrandTable(NetBoxTable):
    name = tables.Column(
        linkify=True,
    )
    domain_count = columns.LinkedCountColumn(
        viewname='wim:domain_list',
        url_params={'brand_id': 'pk'},
        verbose_name="Domains",
    )

    class Meta(NetBoxTable.Meta):
        model = Brand
        # exclude = ('id',)
        fields = (
            'pk', 'id', 'name',
            'domain_count',
            'fqdn_count',
        )
        default_columns = ('name', 'domain_count', 'fqdn_count')
