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
    # -- Choices --
    status = columns.ChoiceFieldColumn()
    asset_class = columns.ChoiceFieldColumn()
    asset_confidence = columns.ChoiceFieldColumn()
    fqdn_status = columns.ChoiceFieldColumn(verbose_name=_('FQDN Status'))
    website_status = columns.ChoiceFieldColumn(verbose_name=_('Website Status'))
    website_role = columns.ChoiceFieldColumn()
    redirect_health = columns.ChoiceFieldColumn()
    # compliance_programs_choice = columns.ChoiceFieldColumn()

    # -- Bools --
    mark_triaging = columns.BooleanColumn(verbose_name="Triaging")
    is_in_cmdb = columns.BooleanColumn(verbose_name="In CMDB")
    is_internet_facing = columns.BooleanColumn(verbose_name="Internet Facing")
    is_flagship = columns.BooleanColumn(verbose_name="Flagship")
    is_nonprod_mirror = columns.BooleanColumn(verbose_name="Is Nonprod Mirror")
    is_cloud_hosted = columns.BooleanColumn(verbose_name="Cloud Hosted")
    is_vendor_managed = columns.BooleanColumn(verbose_name="Vendor Managed")
    is_vendor_hosted = columns.BooleanColumn(verbose_name="Vendor Hosted")
    had_bugbounty = columns.BooleanColumn(verbose_name="Had BB")
    is_risky = columns.BooleanColumn(verbose_name="Risky")
    feature_acct_mgmt = columns.BooleanColumn(verbose_name="Acct Mgmt")
    feature_auth_self_registration = columns.BooleanColumn(verbose_name="Self Registration")
    feature_api = columns.BooleanColumn(verbose_name="Has API")
    is_compliance_required = columns.BooleanColumn(verbose_name="Compliance Required")

    # -- M2M --
    # compliance_programs = tables.ManyToManyColumn(
    #     linkify_item=False,
    #     orderable=False,
    #     verbose_name="Program"
    # )
    software = columns.ManyToManyColumn(
        linkify_item=True,
        verbose_name='Software',
    )
    software_count = columns.LinkedCountColumn(
        accessor=tables.A('software__count'),
        viewname='wim:software_list',
        url_params={'software_id': 'pk'},
        verbose_name='Software Count',
    )

    # -- Text -- Can use either Markdown or Char
    notes = columns.MarkdownColumn()
    vendor_notes = columns.MarkdownColumn()
    comments = columns.MarkdownColumn()
    tags = columns.TagColumn(url_name='wim:fqdn_list')

    class Meta(NetBoxTable.Meta):
        model = FQDN
        # exclude = ('id',)
        fields = (
            "name", "id",
            "mark_triaging", "asset_confidence",
            "status", "status_reason",
            'date_last_recon',
            'fqdn_status', 'website_status',
            'asset_class', 'domain',
            'owners_orig', 'impacted_group_orig', 'impacted_division_orig',
            # 'owners_nb',
            'brand',
            'geo_region_choice', 'geo_region',
            'location_orig', 'location',
            'env_model', 'architectural_model',
            'is_flagship', 'is_in_cmdb',
            'is_nonprod_mirror',
            'had_bugbounty', 'is_risky',
            'public_ip_1', 'ipaddress_public_8',
            'private_ip_1', 'private_ip_2',
            'ipaddress_private_8',
            'hostname_orig',
            'os_char',
            'os_1', 'os_8',
            'criticality_score_1',
            'vuln_scan_coverage', 'date_last_vulnscan',
            'date_last_pentest', 'pentest_priority',
            'risk_analysis_notes',
            'is_compliance_required', 'compliance_programs_choice',
            'tech_webserver_orig',
            # 'tech_webserver_1',
            'tech_addtl',
            'software', 'software_count',
            'is_cloud_hosted', 'cloud_provider',
            'is_akamai', 'is_load_protected', 'is_waf_protected',
            'website_role',
            'website_url', 'website_title', 'website_email_orig',
            'site_operation_age',
            'redirect_health', 'redirect_url',
            'is_vendor_managed', 'is_vendor_hosted',
            'vendor_company_orig', 'vendor_company_fk', 'vendor_pocs_orig',
            'vendor_url', 'vendor_notes',
            'feature_acct_mgmt', 'feature_webauth_type', 'feature_auth_self_registration',
            'feature_api',
            'scoping_size', 'scoping_complexity', 'scoping_roles', 'calc_loe',
            'cnames', 'dns_a_record_ips',
            'tls_protocol_version', 'tls_cert_info', 'tls_cert_expires',
            'tls_cert_is_wildcard', 'tls_cert_self_signed', 'tls_cert_sha1',
            'is_vhost', 'is_http2',
            'response_code', 'content_length',
            'is_internet_facing',
            'tenant',
            'support_group_website_technical_orig', 'support_group_website_approvals_orig',
            # support_group FK's go here
            'notes',
            'tags', 'created', 'last_updated', 'date_created', 'date_modified',
            # 'slug',
        )
        default_columns = (
            'name', 'id', 'status', 'asset_confidence', 'fqdn_status', 'website_status',
            'impacted_group_orig', 'impacted_division_orig', 'location_orig',
            'public_ip_1', 'had_bugbounty', 'is_risky',
            'owners_orig',
        )


