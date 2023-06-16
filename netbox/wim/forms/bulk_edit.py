from django import forms
from django.utils.translation import gettext as _

from dcim.models import Region, Site, SiteGroup
from ipam.choices import *
from ipam.constants import *
from ipam.models import *
from ipam.models import ASN
from netbox.forms import NetBoxModelBulkEditForm
from tenancy.models import Tenant
from utilities.forms import add_blank_choice
from utilities.forms.fields import (
    CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField, NumericArrayField,
)
from utilities.forms.widgets import BulkEditNullBooleanSelect
from wim.models import *
from wim.choices import *


__all__ = (
    'FQDNBulkEditForm',
    'DomainBulkEditForm',
    'BusinessGroupBulkEditForm',
    'BusinessDivisionBulkEditForm',
    'OperatingSystemBulkEditForm',
    'SiteLocationBulkEditForm',
    'VendorBulkEditForm',
    'WebserverFrameworkBulkEditForm',
)


class DomainBulkEditForm(NetBoxModelBulkEditForm):
    model = Domain

    status = forms.ChoiceField(choices=DomainStatusChoices)

    date_last_recon_scanned = forms.DateField()

    # comments = CommentField(label='Comments')

    fieldsets = (
        (None, (
            'status', 'asset_confidence', 'ownership_type',
            'meets_standards',
            'date_last_recon_scanned',
        )),
    )
    # nullable_fields = ('tenant', 'comments')


class FQDNBulkEditForm(NetBoxModelBulkEditForm):
    model = FQDN

    # -- Choices --
    # status = forms.ChoiceField(
    #   choices=add_blank_choice(FQDNStatusChoices),
    #   required=False,
    # )
    # asset_confidence = forms.ChoiceField(choices=AssetConfidenceChoices)
    # fqdn_status = forms.ChoiceField(choices=FQDNOpsStatusChoices)
    # website_status = forms.ChoiceField(choices=WebsiteOpsStatusChoices)

    # -- Bools --
    # NOTE: NetBox approach is this:
    #       - the model def is a "BooleanField" with default=False
    #       - then, forms use this "NullBooleanField"
    mark_triaging = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect(),
        label=_('Triaging'),
    )

    # -- FKs --
    impacted_group_orig = DynamicModelChoiceField(
        queryset=BusinessGroup.objects.all(),
        required=False,
        label=_('Group'),
    )
    impacted_division_orig = DynamicModelChoiceField(
        queryset=BusinessDivision.objects.all(),
        required=False,
        label=_('Division'),
    )
    # location_orig = DynamicModelChoiceField(
    #     queryset=SiteLocation.objects.all(),
    # )
    # location = DynamicModelChoiceField(
    #     queryset=Site.objects.all(),
    # )

    owners_orig = forms.CharField(
        required=False,
        label=_('Owners (Orig)'),
    )

    # tenant = DynamicModelChoiceField(
    #     queryset=Tenant.objects.all(),
    #     required=False
    # )
    
    # -- NetBox Built-In Fields --
    description = forms.CharField(
        max_length=255,
        required=False,
    )
    comments = CommentField()

    fieldsets = (
        ("Edit Ownership", (
            # 'status', 'asset_confidence',
            # 'impacted_group_orig', 'impacted_division_orig',
            # 'owners_orig',
            # 'tenant',
            "mark_triaging",
        )),
        # (None, (
        #     "mark_triaging",
        # )),
    )
    nullable_fields = ('description', 'comments')


class BusinessGroupBulkEditForm(NetBoxModelBulkEditForm):
    model = BusinessGroup


class BusinessDivisionBulkEditForm(NetBoxModelBulkEditForm):
    model = BusinessDivision


class OperatingSystemBulkEditForm(NetBoxModelBulkEditForm):
    model = OperatingSystem


class SiteLocationBulkEditForm(NetBoxModelBulkEditForm):
    model = SiteLocation


class VendorBulkEditForm(NetBoxModelBulkEditForm):
    model = Vendor


class WebserverFrameworkBulkEditForm(NetBoxModelBulkEditForm):
    model = WebserverFramework
