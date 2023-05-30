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

__all__ = (
    'FQDNBulkEditForm',
    'DomainBulkEditForm',
    # 'IPAddressBulkEditForm',
    # 'IPRangeBulkEditForm',
    # 'PrefixBulkEditForm',
    # 'RoleBulkEditForm',
    # 'ServiceBulkEditForm',
    # 'ServiceTemplateBulkEditForm',
)


class DomainBulkEditForm(NetBoxModelBulkEditForm):
    pass

class FQDNBulkEditForm(NetBoxModelBulkEditForm):
    pass




# class AggregateBulkEditForm(NetBoxModelBulkEditForm):
#     rir = DynamicModelChoiceField(
#         queryset=RIR.objects.all(),
#         required=False,
#         label=_('RIR')
#     )
#     tenant = DynamicModelChoiceField(
#         queryset=Tenant.objects.all(),
#         required=False
#     )
#     date_added = forms.DateField(
#         required=False
#     )
#     description = forms.CharField(
#         max_length=200,
#         required=False
#     )
#     comments = CommentField(
#         label='Comments'
#     )

#     model = Aggregate
#     fieldsets = (
#         (None, ('rir', 'tenant', 'date_added', 'description')),
#     )
#     nullable_fields = ('date_added', 'description', 'comments')


# class RoleBulkEditForm(NetBoxModelBulkEditForm):
#     weight = forms.IntegerField(
#         required=False
#     )
#     description = forms.CharField(
#         max_length=200,
#         required=False
#     )

#     model = Role
#     fieldsets = (
#         (None, ('weight', 'description')),
#     )
#     nullable_fields = ('description',)



# class IPRangeBulkEditForm(NetBoxModelBulkEditForm):
#     vrf = DynamicModelChoiceField(
#         queryset=VRF.objects.all(),
#         required=False,
#         label=_('VRF')
#     )
#     tenant = DynamicModelChoiceField(
#         queryset=Tenant.objects.all(),
#         required=False
#     )
#     status = forms.ChoiceField(
#         choices=add_blank_choice(IPRangeStatusChoices),
#         required=False
#     )
#     role = DynamicModelChoiceField(
#         queryset=Role.objects.all(),
#         required=False
#     )
#     mark_utilized = forms.NullBooleanField(
#         required=False,
#         widget=BulkEditNullBooleanSelect(),
#         label=_('Treat as 100% utilized')
#     )
#     description = forms.CharField(
#         max_length=200,
#         required=False
#     )
#     comments = CommentField(
#         label='Comments'
#     )

#     model = IPRange
#     fieldsets = (
#         (None, ('status', 'role', 'vrf', 'tenant', 'mark_utilized', 'description')),
#     )
#     nullable_fields = (
#         'vrf', 'tenant', 'role', 'description', 'comments',
#     )


# class IPAddressBulkEditForm(NetBoxModelBulkEditForm):
#     vrf = DynamicModelChoiceField(
#         queryset=VRF.objects.all(),
#         required=False,
#         label=_('VRF')
#     )
#     mask_length = forms.IntegerField(
#         min_value=IPADDRESS_MASK_LENGTH_MIN,
#         max_value=IPADDRESS_MASK_LENGTH_MAX,
#         required=False
#     )
#     tenant = DynamicModelChoiceField(
#         queryset=Tenant.objects.all(),
#         required=False
#     )
#     status = forms.ChoiceField(
#         choices=add_blank_choice(IPAddressStatusChoices),
#         required=False
#     )
#     role = forms.ChoiceField(
#         choices=add_blank_choice(IPAddressRoleChoices),
#         required=False
#     )
#     dns_name = forms.CharField(
#         max_length=255,
#         required=False,
#         label=_('DNS name')
#     )
#     description = forms.CharField(
#         max_length=200,
#         required=False
#     )
#     comments = CommentField(
#         label='Comments'
#     )

#     model = IPAddress
#     fieldsets = (
#         (None, ('status', 'role', 'tenant', 'description')),
#         ('Addressing', ('vrf', 'mask_length', 'dns_name')),
#     )
#     nullable_fields = (
#         'vrf', 'role', 'tenant', 'dns_name', 'description', 'comments',
#     )




# class ServiceTemplateBulkEditForm(NetBoxModelBulkEditForm):
#     protocol = forms.ChoiceField(
#         choices=add_blank_choice(ServiceProtocolChoices),
#         required=False
#     )
#     ports = NumericArrayField(
#         base_field=forms.IntegerField(
#             min_value=SERVICE_PORT_MIN,
#             max_value=SERVICE_PORT_MAX
#         ),
#         required=False
#     )
#     description = forms.CharField(
#         max_length=200,
#         required=False
#     )
#     comments = CommentField(
#         label='Comments'
#     )

#     model = ServiceTemplate
#     fieldsets = (
#         (None, ('protocol', 'ports', 'description')),
#     )
#     nullable_fields = ('description', 'comments')


# class ServiceBulkEditForm(ServiceTemplateBulkEditForm):
#     model = Service

