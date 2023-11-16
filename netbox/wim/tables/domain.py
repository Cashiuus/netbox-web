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
    # -- FKs --
    brand = tables.Column(linkify=True)

    # -- Related Object Count Handlers --
    fqdn_count = columns.LinkedCountColumn(
        viewname='wim:fqdn_list',
        url_params={'domain_id': 'pk'},
        verbose_name=_('FQDN Count')
    )

    # -- Choices --
    status = columns.ChoiceFieldColumn()
    # ownership_type = columns.ChoiceFieldColumn()

    # -- Bools --
    meets_standards = columns.BooleanColumn()

    tenant = TenantColumn()
    notes = columns.MarkdownColumn()
    tags = columns.TagColumn(
        url_name='wim:domain_list'
    )

    class Meta(NetBoxTable.Meta):
        model = Domain
        # exclude = ('id',)
        fields = (
            'name', 'id', 'fqdn_count',
            'status', 'asset_confidence',
            'brand', 'ownership_type',
            'date_first_registered', 'date_registrar_expiry',
            'date_last_recon_scanned',
            'meets_standards', 'is_flagship', 'is_internet_facing',
            'registrar_company_orig',
            'registrant_org', 'registration_emails_orig', 'registration_emails',
            'nameservers', 'registrar_domain_statuses',
            'mail_servers', 'whois_servers',
            'soa_nameservers', 'soa_email',
            'notes',
            'tenant',
            'tags', 'created', 'last_updated', 'date_created', 'date_modified',
        )
        default_columns = (
            'name', 'id', 'status',
            'ownership_type',
            'date_first_registered', 'date_registrar_expiry',
            'date_last_recon_scanned',
            'fqdn_count', 'brand',
            'meets_standards',
            'registrar_company_orig', 'registrant_org',
        )
