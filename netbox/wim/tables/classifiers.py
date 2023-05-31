import django_tables2 as tables
from django.utils.translation import gettext as _

from netbox.tables import NetBoxTable, columns
from tenancy.tables import TenancyColumnsMixin, TenantColumn
from wim.models import *


__all__ = (
    'BusinessGroupTable',
    'OperatingSystemTable',
)


class BusinessGroupTable(TenancyColumnsMixin, NetBoxTable):

    status = columns.ChoiceFieldColumn()

    is_ = columns.BooleanColumn(verbose_name="")

    notes = columns.MarkdownColumn()
    tags = columns.TagColumn(
        url_name='wim:BusinessGroup_list'
    )

    class Meta:
        model = BusinessGroup
        exclude = ('id',)
        fields = (
            'pk', 'name',
        )
        default_columns = ('pk', 'name')






class OperatingSystemTable(TenancyColumnsMixin, NetBoxTable):

    status = columns.ChoiceFieldColumn()

    is_ = columns.BooleanColumn(verbose_name="")

    m2m_field = tables.ManyToManyColumn(
        linkify_item=False,
        orderable=False,
        verbose_name=""
    )

    notes = columns.MarkdownColumn()
    tags = columns.TagColumn(
        url_name='wim:OperatingSystem_list'
    )

    class Meta:
        model = OperatingSystem
        exclude = ('id',)
        fields = (
            'vendor', 'product', 'update', 'build', 'family', 'cpe',

        )
        default_columns = ('vendor', 'product', 'update', 'family', 'build')




