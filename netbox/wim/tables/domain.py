import django_tables2 as tables
from django.utils.translation import gettext as _

from netbox.tables import NetBoxTable, columns
from tenancy.tables import TenancyColumnsMixin, TenantColumn
from wim.models import *

__all__ = (
    'DomainTable',
)


class DomainTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    status = columns.ChoiceFieldColumn()

    fqdn_count = columns.LinkedCountColumn(
        viewname='wim:fqdn_list',
        url_params={'domain_id': 'pk'},
        verbose_name=_('FQDN Count')
    )
    meets_standards = columns.BooleanColumn()

    tenant = TenantColumn()
    notes = columns.MarkdownColumn()
    tags = columns.TagColumn(
        url_name='wim:domain_list'
    )

    class Meta(NetBoxTable.Meta):
        model = Domain
        exclude = ('id',)
        fields = (
            'name', 'status', 'date_first_registered', 'date_registrar_expiry',
            'date_last_recon_scanned',
            'meets_standards',
            'registrant_org', 'registration_emails',
            'registrar_company',
            'notes',
            'tags', 'created', 'last_updated', 'date_created', 'date_modified',
        )
        default_columns = (
            'name', 'status', 'date_registrar_expiry', 'date_last_recon_scanned',
            'meets_standards'
        )
