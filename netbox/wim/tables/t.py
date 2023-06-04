import django_tables2 as tables
from django.utils.translation import gettext as _

from netbox.tables import NetBoxTable, columns
from tenancy.tables import TenancyColumnsMixin, TenantColumn
from wim.models import *


__all__ = (
    '{{model_name}}Table',
)


class {{model_name}}Table(TenancyColumnsMixin, NetBoxTable):
    name = tables.Column(linkify=True)

    status = columns.ChoiceFieldColumn()

    is_ = columns.BooleanColumn(verbose_name="")

    m2m_field = tables.ManyToManyColumn(
        linkify_item=False,
        orderable=False,
        verbose_name=""
    )

    notes = columns.MarkdownColumn()
    tags = columns.TagColumn(
        url_name='wim:{{model_name}}_list'
    )

    class Meta(NetBoxTable.Meta):
        model = {{model_name}}
        exclude = ('id',)
        fields = (
            'pk', 'name',
        )
        default_columns = ('pk', 'name')
