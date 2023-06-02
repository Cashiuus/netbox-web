import django_tables2 as tables
from django.utils.translation import gettext as _

from netbox.tables import NetBoxTable, columns
from tenancy.tables import TenancyColumnsMixin, TenantColumn
from wim.models import *


__all__ = (
    'FQDNTable',
)


class FQDNTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    status = columns.ChoiceFieldColumn()
    asset_class = columns.ChoiceFieldColumn()
    role = columns.ChoiceFieldColumn()
    redirect_health = columns.ChoiceFieldColumn()

    is_in_cmdb = columns.BooleanColumn(verbose_name="In CMDB")
    is_internet_facing = columns.BooleanColumn(verbose_name="Internet Facing")
    is_flagship = columns.BooleanColumn(verbose_name="Flagship")
    is_cloud_hosted = columns.BooleanColumn(verbose_name="Cloud Hosted")
    is_vendor_managed = columns.BooleanColumn(verbose_name="Vendor Managed")
    is_vendor_hosted = columns.BooleanColumn(verbose_name="Vendor Hosted")

    had_bugbounty = columns.BooleanColumn(verbose_name="Had BB")
    is_risky = columns.BooleanColumn(verbose_name="Risky")
    feature_acct_mgmt = columns.BooleanColumn(verbose_name="Acct Mgmt")
    feature_auth_self_registration = columns.BooleanColumn(verbose_name="Self Registration")
    feature_api = columns.BooleanColumn(verbose_name="Has API")
    is_compliance_required = columns.BooleanColumn(verbose_name="Compliance Required")

    compliance_programs = tables.ManyToManyColumn(
        linkify_item=False,
        orderable=False,
        verbose_name="Program"
    )
    notes = columns.MarkdownColumn()
    vendor_notes = columns.MarkdownColumn()
    tags = columns.TagColumn(
        url_name='wim:fqdn_list'
    )

    class Meta(NetBoxTable.Meta):
        model = FQDN
        exclude = ('id',)
        fields = (
            'name', 'status', 
            'fqdn_status', 'fqdn_status_orig', 'website_status', 'website_status_orig',
            'domain',
            'owners_orig', 'impacted_group_orig', 'impacted_division_orig',
            'location_orig', 'location',
            'had_bugbounty', 'is_risky',
            'public_ip_1', 'ipaddress_public_8',
            'private_ip_1', 'ipaddress_private_8',
            'hostname_orig',
            'os_1', 'os_8',
            'env_used_for', 'architectural_model',
            'tech_webserver_1', 'tech_addtl',
            'redirect_url',
            'vendor_company_1',
            'is_compliance_required', 'compliance_programs',
            'notes',
            'tags', 'created', 'last_updated', 'date_created', 'date_modified',

        )
        default_columns = (
            'name', 'status', 'fqdn_status', 'website_status', 'owners_orig',
        )


