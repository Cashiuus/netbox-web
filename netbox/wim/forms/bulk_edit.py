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
    'BrandBulkEditForm',
    'CertificateBulkEditForm',
    'FQDNBulkEditForm',
    'DomainBulkEditForm',
    'BusinessGroupBulkEditForm',
    'BusinessDivisionBulkEditForm',
    'OperatingSystemBulkEditForm',
    'SiteLocationBulkEditForm',
    'VendorBulkEditForm',
    'SoftwareBulkEditForm',
)


class CertificateBulkEditForm(NetBoxModelBulkEditForm):
    # -- Choices --
    signing_algorithm = forms.ChoiceField(
        choices=CertSigningAlgorithmChoices,
        required=False,
    )
    key_type = forms.ChoiceField(
        choices=CertSigningAlgorithmChoices,
        required=False,
    )
    key_bitlength = forms.ChoiceField(
        choices=CertSigningAlgorithmChoices,
        required=False,
    )

    model = Certificate
    fieldsets = (
        (None, ('key_bitlength',)),
    )
    # nullable_fields = ('field1',)


class DomainBulkEditForm(NetBoxModelBulkEditForm):

    # -- Choices --
    status = forms.ChoiceField(
        choices=DomainStatusChoices,
        required=False,
    )
    asset_confidence = forms.ChoiceField(
        choices=AssetConfidenceChoices,
        required=False,
    )
    ownership_type = forms.ChoiceField(
        choices=DomainOwnershipStatusChoices,
        required=False,
    )

    # -- Bools --
    meets_standards = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect(),
    )

    # -- Dates --
    date_last_recon_scanned = forms.DateField(required=False)

    # comments = CommentField(label='Comments')
    model = Domain
    fieldsets = (
        (None, (
            'status', 'asset_confidence', 'ownership_type',
            'meets_standards',
            'date_last_recon_scanned',
        )),
    )
    # nullable_fields = ('tenant', 'comments')


class FQDNBulkEditForm(NetBoxModelBulkEditForm):

    # mark_triaging = forms.NullBooleanField(
    #     required=False,
    #     widget=BulkEditNullBooleanSelect(),
    #     label=_('Triaging'),
    # )

    # -- M2M --
    # software = DynamicModelMultipleChoiceField(
    #     queryset=Software.objects.all(),
    #     required=False,
    #     label=_('Software'),
    # )

    # -- NetBox Built-In Fields --
    description = forms.CharField(
        max_length=200,
        required=False,
    )
    # comments field gets defined here, don't include in fieldsets below or
    # it'll show up twice on form
    comments = CommentField()

    model = FQDN
    fieldsets = (
        (None, (
            # 'status', 'asset_confidence',
            # 'impacted_group_orig', 'impacted_division_orig',
            # 'owners_orig',
            # 'tenant',
            # "mark_triaging",
            'description',
        )),
    )
    nullable_fields = ('description', 'comments')


# -- Commented out FQDN stuff while I troubleshoot
    # -- Choices --
    # status = forms.ChoiceField(
    #   choices=add_blank_choice(FQDNStatusChoices),
    #   required=False,
    # )
    # asset_confidence = forms.ChoiceField(
    #     choices=AssetConfidenceChoices,
    #     required=False,
    #     label=_('Asset Confidence'),
    # )
    # fqdn_status = forms.ChoiceField(choices=FQDNOpsStatusChoices)
    # website_status = forms.ChoiceField(choices=WebsiteOpsStatusChoices)

    # -- Bools --
    # NOTE: NetBox approach is this:
    #       - the model def is a "BooleanField" with default=False
    #       - then, forms use this "NullBooleanField"

    # -- FKs --
    # impacted_group_orig = DynamicModelChoiceField(
    #     queryset=BusinessGroup.objects.all(),
    #     required=False,
    #     label=_('Group'),
    # )
    # impacted_division_orig = DynamicModelChoiceField(
    #     queryset=BusinessDivision.objects.all(),
    #     required=False,
    #     label=_('Division'),
    # )
    # location_orig = DynamicModelChoiceField(
    #     queryset=SiteLocation.objects.all(),
    # )
    # location = DynamicModelChoiceField(
    #     queryset=Site.objects.all(),
    # )

    # owners_orig = forms.CharField(
    #     required=False,
    #     label=_('Owners (Orig)'),
    # )

    # tenant = DynamicModelChoiceField(
    #     queryset=Tenant.objects.all(),
    #     required=False
    # )


class BrandBulkEditForm(NetBoxModelBulkEditForm):
    model = Brand


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


class SoftwareBulkEditForm(NetBoxModelBulkEditForm):
    model = Software
