from django import forms
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


__all__ = (
    'DomainFilterForm',
    'FQDNFilterForm',
    'BusinessGroupFilterForm',
    'BusinessDivisionFilterForm',
    'OperatingSystemFilterForm',
    'SiteLocationFilterForm',
    'VendorFilterForm',
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


class FQDNFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    model = FQDN


class BusinessGroupFilterForm(NetBoxModelFilterSetForm):
    model = BusinessGroup


class BusinessDivisionFilterForm(NetBoxModelFilterSetForm):
    model = BusinessDivision


class OperatingSystemFilterForm(NetBoxModelFilterSetForm):
    model = OperatingSystem


class SiteLocationFilterForm(NetBoxModelFilterSetForm):
    model = SiteLocation


class VendorFilterForm(NetBoxModelFilterSetForm):
    model = Vendor


class WebserverFrameworkFilterForm(NetBoxModelFilterSetForm):
    model = WebserverFramework

