from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from dcim.models import Site
from wim.choices import *
from wim.constants import *
from wim.models import *
from netbox.forms import NetBoxModelImportForm
from tenancy.models import Tenant
from utilities.forms.fields import CSVChoiceField, CSVContentTypeField, CSVModelChoiceField, SlugField


__all__ = (
    'DomainImportForm',
    'FQDNImportForm',
    'BusinessGroupImportForm',
    'BusinessDivisionImportForm',
    'OperatingSystemImportForm',
    'SiteLocationImportForm',
    'VendorImportForm',
    'WebserverFrameworkImportForm',
)


class DomainImportForm(NetBoxModelImportForm):
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Assigned tenant')
    )

    # registrar_company = CSVModelChoiceField(
    #     queryset=Registrar.objects.all(),
    #     required=False,
    #     to_field_name='name',
    #     # help_text=_('Regisrar company name')
    # )

    # -- Choices Fields --
    status = CSVChoiceField(
        choices=DomainStatusChoices,
    )

    # -- M2M Fields --
    # TODO: Unsure how to configure a ManyToMany field for bulk import
    # registration_emails = 


    class Meta:
        model = Domain
        # fields = ('name', 'tenant')
        fields = [
            'name', 'status_orig', 'status', 
            'confidence', 'meets_standards',
            'tenant',
            'date_registrar_expiry', 'date_first_registered',
            'date_last_recon_scanned',
            'is_internet_facing', 'is_flagship',
            'registrar_company_orig', 'registrar_iana_id_orig',
            'registrar_domain_statuses',
            'registrant_org',
            'registration_emails_orig', 'registration_emails',
            'nameservers', 'mail_servers', 'whois_servers',
            'soa_nameservers', 'soa_email',
            'notes',
        ]



class FQDNImportForm(NetBoxModelImportForm):
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Assigned tenant')
    )

    class Meta:
        model = FQDN
        fields = ('name', 'ipaddress_public_8', 'tenant')


class BusinessGroupImportForm(NetBoxModelImportForm):
    # principal_location_orig = CSVModelChoiceField(
    #     queryset = SiteLocation.objects.all(),
    #     to_field_name="code",
    # )
    # principal_location_nb = CSVModelChoiceField(
    #     queryset=Site.objects.all(),
    #     to_field_name='name',
    # )

    slug = SlugField()

    class Meta:
        model = BusinessGroup
        fields = (
            'name', 'slug', 'acronym', 'description',
            'principal_location_orig', 'principal_location_nb',
        )


class BusinessDivisionImportForm(NetBoxModelImportForm):

    group = CSVModelChoiceField(
        queryset=BusinessGroup.objects.all(),
        required=True,
        to_field_name="acronym",
        help_text='Linked/Parent Business group acronym'
    )
    principal_location_orig = CSVModelChoiceField(
        queryset=SiteLocation.objects.all(),
        to_field_name='code',
        required=False,
        help_text='Linked site location code'
    )

    class Meta:
        model = BusinessDivision
        fields = (
            'name', 'slug', 'acronym', 'group', 'description',
            'principal_location_orig', 
        )


class OperatingSystemImportForm(NetBoxModelImportForm):

    class Meta:
        model = OperatingSystem
        fields = ('vendor', 'product', 'update')


class SiteLocationImportForm(NetBoxModelImportForm):
    # Testing to import my original choices, which are done differently
    # geo_region_orig = Field(attribute="get_geo_region_display")

    geo_region_choice = CSVChoiceField(
        choices=GeoRegionChoices,
        help_text=_('Geographic Region from choices')
    )

    class Meta:
        model = SiteLocation
        fields = (
            'name', 'slug', 'code', 'geo_region_choice',
            # 'impacted_group_orig', 'impacted_division_orig',
            'priority', 'street', 'city', 'state', 'country_1', 
            'timezone_1', 'timezone', 'it_infra_contact', 'ranges_tmp1', 
            'notes'
        )


class VendorImportForm(NetBoxModelImportForm):

    class Meta:
        model = Vendor
        fields = ('name',)


class WebserverFrameworkImportForm(NetBoxModelImportForm):

    class Meta:
        model = WebserverFramework
        fields = ('name', 'product', 'version', 'raw_banner', 'cpe')


