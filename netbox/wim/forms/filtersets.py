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
    'DomainFilterForm',
    'FQDNFilterForm',
    'BusinessGroupFilterForm',
    'BusinessDivisionFilterForm',
    'OperatingSystemFilterForm',
    'SiteLocationFilterForm',
    'VendorFilterForm',
    'WebEmailFilterForm',
    'WebserverFrameworkFilterForm',
)

# PREFIX_MASK_LENGTH_CHOICES = add_blank_choice([
#     (i, i) for i in range(PREFIX_LENGTH_MIN, PREFIX_LENGTH_MAX + 1)
# ])

# IPADDRESS_MASK_LENGTH_CHOICES = add_blank_choice([
#     (i, i) for i in range(IPADDRESS_MASK_LENGTH_MIN, IPADDRESS_MASK_LENGTH_MAX + 1)
# ])


class DomainFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    model = Domain

    # -- Choices --
    status = forms.MultipleChoiceField(
        choices=add_blank_choice(DomainStatusChoices),
        required=False
    )
    confidence = forms.MultipleChoiceField(
        choices=add_blank_choice(AssetConfidenceChoices),
        required=False
    )

    date_registrar_expiry = forms.DateField(required=False, widget=DatePicker())
    date_last_recon_scanned = forms.DateField(required=False, widget=DatePicker())

    last_scanned__before = forms.DateField(
        required=False,
        widget=DatePicker()
    )

    expires__before = forms.DateField(
        required=False,
        widget=DatePicker()
    )

    meets_standards = forms.NullBooleanField(
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES)
    )
    # -- FKs --

    tag = TagFilterField(model)

    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        ('Filter by Status', ('status', 'confidence', 'meets_standards')),
        ('Filter by Date', (
            'date_registrar_expiry', 'date_last_recon_scanned',
            'last_scanned__before', 'expires__before',
        )),
        ('Filter by Business', ('tenant_group_id', 'tenant_id')),
    )


class FQDNFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    model = FQDN

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

    # -- Booleans --
    mark_triaging = forms.BooleanField(
        required=False,
        label=_('Marked Triaging'),
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

    # -- FKs --
    impacted_group_orig = DynamicModelMultipleChoiceField(
        queryset=BusinessGroup.objects.all(),
        required=False,
        label=_('Impacted BU Group')
    )
    impacted_division_orig = DynamicModelMultipleChoiceField(
        queryset=BusinessDivision.objects.all(),
        required=False,
        label=_('Impacted BU Division')
    )
    location_orig = DynamicModelMultipleChoiceField(
        queryset=SiteLocation.objects.all(),
        required=False,
        label=_('Location (Orig)'),
    )
    location = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label=_('Location (NB)'),
    )

    # -- User model --
    # user = DynamicModelMultipleChoiceField(
    #     queryset=User.objects.all(),
    #     required=False,
    #     label=_('User'),
    #     widget=APISelectMultiple(api_url='/api/users/users/')
    # )

    tag = TagFilterField(model)

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
    webserverframework_id = DynamicModelMultipleChoiceField(
        queryset=WebserverFramework.objects.all(),
        required=False,
        label=_('Web Framework'),
    )

    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        ("Filters", (
            'mark_triaging', 
            'domain_id',
            'status',
            'asset_confidence', 'asset_class',
            'fqdn_status', 'website_status',
            'is_in_cmdb', 'is_flagship',
            'is_nonprod_mirror',
        )),
        ('Filter by Business', (
            # 'impacted_group_orig', 'impacted_division_orig',
            'businessgroup_id', 'businessdivision_id',
            'location_orig', 'location',
            'tenant_group_id', 'tenant_id',
            'vendor_id',
        )),
        ('Filter by Security Criteria', (
            'compliance_programs_choice',
        ))
    )


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


class VendorFilterForm(NetBoxModelFilterSetForm):
    model = Vendor

    name = forms.CharField()

    fieldsets = (
        (None, ('q', 'filter_id')),
        ("Filter by", (
            'name',
        )),
    )


class WebEmailFilterForm(NetBoxModelFilterSetForm):
    model = WebEmail


class WebserverFrameworkFilterForm(NetBoxModelFilterSetForm):
    model = WebserverFramework

