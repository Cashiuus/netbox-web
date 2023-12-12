from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _

from dcim.models import Location, Rack, Region, Site, SiteGroup, Device
from wim.choices import *
from wim.constants import *
from wim.models import *
from netbox.forms import NetBoxModelFilterSetForm
from tenancy.forms import TenancyFilterForm
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, add_blank_choice
from utilities.forms.fields import (
    ContentTypeMultipleChoiceField, DynamicModelChoiceField, DynamicModelMultipleChoiceField, TagFilterField,
)
from utilities.forms.widgets import APISelectMultiple, DatePicker, DateTimePicker


__all__ = (
    'BrandFilterForm',
    'BusinessGroupFilterForm',
    'BusinessDivisionFilterForm',
    'CertificateFilterForm',
    'DomainFilterForm',
    'FQDNFilterForm',
    'OperatingSystemFilterForm',
    'SiteLocationFilterForm',
    'SoftwareFilterForm',
    'VendorFilterForm',
    'WebEmailFilterForm',
)


# PREFIX_MASK_LENGTH_CHOICES = add_blank_choice([
#     (i, i) for i in range(PREFIX_LENGTH_MIN, PREFIX_LENGTH_MAX + 1)
# ])

# IPADDRESS_MASK_LENGTH_CHOICES = add_blank_choice([
#     (i, i) for i in range(IPADDRESS_MASK_LENGTH_MIN, IPADDRESS_MASK_LENGTH_MAX + 1)
# ])


class CertificateFilterForm(NetBoxModelFilterSetForm):
    model = Certificate

    # -- Choices --
    signing_algorithm = forms.MultipleChoiceField(
        choices=add_blank_choice(CertSigningAlgorithmChoices),
        required=False,
    )
    key_bitlength = forms.MultipleChoiceField(
        choices=add_blank_choice(CertBitLengthChoices),
        required=False,
    )
    # -- Dates -- Only have to define custom date fields, not model date fields
    date_expiration__before = forms.DateField(
        required=False,
        widget=DatePicker(),
    )

    # NOTE: Only put custom dates here, unless you want to be able to filter
    # on a single exact date of the year.
    fieldsets = (
        (None, ('q', 'filter_id')),
        ("Filter by Fields", (
            "signing_algorithm", "key_bitlength",
        )),
        ("Filter By Date", (
            "date_expiration__before",
        )),
    )



class DomainFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    model = Domain

    # -- Choices --
    status = forms.MultipleChoiceField(
        choices=add_blank_choice(DomainStatusChoices),
        required=False,
    )
    asset_confidence = forms.MultipleChoiceField(
        choices=add_blank_choice(AssetConfidenceChoices),
        required=False,
    )
    ownership_type = forms.MultipleChoiceField(
        choices=add_blank_choice(DomainOwnershipStatusChoices),
        required=False,
    )
    # -- Dates -- Only have to define custom date fields, not model date fields
    date_last_recon_scanned__before = forms.DateField(
        required=False,
        widget=DatePicker(),
    )
    date_registrar_expiry__before = forms.DateField(
        required=False,
        widget=DatePicker(),
    )
    # -- Bools --
    meets_standards = forms.NullBooleanField(
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
    # -- FKs --
    brand_id = DynamicModelMultipleChoiceField(
        queryset=Brand.objects.all(),
        required=False,
        label=_('Brand/Acquisition'),
    )

    tag = TagFilterField(model)

    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        ('Filter by Fields', (
            'status', 'asset_confidence', 'ownership_type',
            'meets_standards',
            'tenant_group_id', 'tenant_id', 'brand_id',
        )),
        ('Filter by Date', (
            'date_last_recon_scanned__before', 'date_registrar_expiry__before',
        )),
    )


class FQDNFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    model = FQDN
    tag = TagFilterField(model)

    # -- Choices --
    status = forms.MultipleChoiceField(
        choices=FQDNStatusChoices,
        required=False
    )
    fqdn_status = forms.MultipleChoiceField(
        choices=FQDNOpsStatusChoices,
        required=False,
        label=_('FQDN Technical Status'),
    )
    website_status = forms.MultipleChoiceField(
        choices=WebsiteOpsStatusChoices,
        required=False,
        label=_('Website Technical Status'),
    )
    asset_confidence = forms.MultipleChoiceField(
        choices=AssetConfidenceChoices,
        required=False,
    )
    asset_class = forms.MultipleChoiceField(
        choices=AssetClassChoices,
        required=False,
    )
    compliance_programs_choice = forms.MultipleChoiceField(
        choices=ComplianceProgramChoices,
        required=False,
        label=_('Compliance Programs'),
    )
    geo_region_choice = forms.MultipleChoiceField(
        choices=GeoRegionChoices,
        required=False,
        label=_('Geo Region (choice)'),
    )
    tls_protocol_version = forms.MultipleChoiceField(
        choices=TransportLayerSecurityVersionChoices,
        required=False,
        label=_('TLS Protocol Version'),
    )

    # -- Booleans --
    mark_triaging = forms.BooleanField(
        required=False,
        label=_('Marked Triaging'),
        widget=forms.RadioSelect(
            choices=((True, "Yes"), (False, "No"))
        ),
    )
    is_risky = forms.BooleanField(
        required=False,
        label=_('Is Risky'),
        widget=forms.RadioSelect(
            choices=((True, "Yes"), (False, "No"))
        ),
    )
    had_bugbounty = forms.BooleanField(
        required=False,
        label=_('Had Bug Bounty Submission'),
        widget=forms.RadioSelect(
            choices=((True, "Yes"), (False, "No"))
        ),
    )
    vuln_scan_coverage = forms.BooleanField(
        required=False,
        label=_('Vuln Scanner Coverage'),
        widget=forms.RadioSelect(
            choices=((True, "Yes"), (False, "No"))
        ),
    )
    is_in_cmdb = forms.BooleanField(
        required=False,
        label=_('Is In CMDB'),
        widget=forms.RadioSelect(
            choices=((True, "Yes"), (False, "No"))
        ),
    )
    is_flagship = forms.BooleanField(
        required=False,
        label=_('Flagship'),
        widget=forms.RadioSelect(
            choices=((True, "Yes"), (False, "No"))
        ),
    )
    is_nonprod_mirror = forms.BooleanField(
        required=False,
        label=_('Is Nonprod Mirror'),
        widget=forms.RadioSelect(
            choices=((True, "Yes"), (False, "No"))
        ),
    )
    tls_cert_self_signed = forms.BooleanField(
        required=False,
        label=_('TLS Cert Is Self-Signed'),
        widget=forms.RadioSelect(
            choices=((True, "Yes"), (False, "No"))
        ),
    )
    is_vendor_managed = forms.BooleanField(
        required=False,
        label=_('Vendor Managed'),
        widget=forms.RadioSelect(
            choices=((True, "Yes"), (False, "No"))
        ),
    )

    # -- Dates --
    tls_cert_expires__before = forms.DateField(
        required=False,
        label=_('TLS Cert Expires Before'),
        widget=DatePicker(),
    )
    date_last_recon__before = forms.DateField(
        required=False,
        label=_('Last Recon Before'),
        widget=DatePicker(),
    )

    # -- FKs + Serializers --
    # NOTE: Making this a single choice field on purpose, rest are multiple
    certificate_id = DynamicModelChoiceField(
        queryset=Certificate.objects.all(),
        required=False,
        label=_('TLS Certificate'),
    )
    location_orig_id = DynamicModelMultipleChoiceField(
        queryset=SiteLocation.objects.all(),
        required=False,
        label=_('Location (Orig)'),
    )
    location_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label=_('Location (NB)'),
    )
    # -- Related Objects Handlers/Filters --
    domain_id = DynamicModelMultipleChoiceField(
        queryset=Domain.objects.all(),
        required=False,
        label=_('Domain'),
    )
    businessgroup_id = DynamicModelMultipleChoiceField(
        queryset=BusinessGroup.objects.all(),
        required=False,
        label=_('Org Group'),
    )
    businessdivision_id = DynamicModelMultipleChoiceField(
        queryset=BusinessDivision.objects.all(),
        required=False,
        label=_('Org Division'),
    )
    vendor_id = DynamicModelMultipleChoiceField(
        queryset=Vendor.objects.all(),
        required=False,
        label=_('Vendor'),
    )
    # -- Software M2M --
    software_id = DynamicModelMultipleChoiceField(
        queryset=Software.objects.all(),
        required=False,
        label=_('Software'),
    )
    # -- User model --
    # user = DynamicModelMultipleChoiceField(
    #     queryset=User.objects.all(),
    #     required=False,
    #     label=_('User'),
    #     widget=APISelectMultiple(api_url='/api/users/users/')
    # )

    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        ("Status", (
            'mark_triaging',
            'status',
            'asset_confidence',
            'fqdn_status', 'website_status',
        )),
        ('Security', (
            'is_risky', 'had_bugbounty',
            'vuln_scan_coverage',
            'date_last_recon__before',
            'tls_protocol_version', 'certificate_id',
            'tls_cert_self_signed',
            'tls_cert_expires__before',
            'compliance_programs_choice',
        )),
        ('Attributes', (
            'domain_id',
            'software_id',
            'asset_class',
            'is_in_cmdb', 'is_flagship',
            'is_nonprod_mirror',
        )),
        ('Business', (
            'geo_region_choice',
            'location_orig_id', 'location_id',
            'businessgroup_id', 'businessdivision_id',
            'tenant_group_id', 'tenant_id',
            'vendor_id',
            'is_vendor_managed',
        )),
    )


class BrandFilterForm(NetBoxModelFilterSetForm):
    model = Brand


class BusinessGroupFilterForm(NetBoxModelFilterSetForm):
    model = BusinessGroup


class BusinessDivisionFilterForm(NetBoxModelFilterSetForm):
    model = BusinessDivision


class OperatingSystemFilterForm(NetBoxModelFilterSetForm):
    model = OperatingSystem

    platform_family = forms.MultipleChoiceField(
        choices=PlatformFamilyChoices,
        required=False,
    )
    platform_type = forms.MultipleChoiceField(
        choices=PlatformTypeChoices,
        required=False,
    )

    fieldsets = (
        (None, ('q', 'filter_id')),
        ("Filter by", (
            "platform_family", "platform_type",
        )),
    )
    # 'vendor', 'product', 'update',
    # 'platform_family', 'platform_type',
    # 'build_number', 'cpe', 'color',


class SiteLocationFilterForm(NetBoxModelFilterSetForm):
    model = SiteLocation
    tag = TagFilterField(model)


class SoftwareFilterForm(NetBoxModelFilterSetForm):
    model = Software

    # name = forms.CharField(required=False)
    # product = forms.CharField(required=False)

    fieldsets = (
        (None, ('q', 'filter_id')),
    )


class VendorFilterForm(NetBoxModelFilterSetForm):
    model = Vendor
    name = forms.CharField(required=False)

    fieldsets = (
        (None, ('q', 'filter_id')),
        ("Filter by", (
            'name',
        )),
    )


class WebEmailFilterForm(NetBoxModelFilterSetForm):
    model = WebEmail
