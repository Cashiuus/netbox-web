# from django.contrib.contenttypes.models import ContentType
# from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from netbox.api.fields import ChoiceField, ContentTypeField, SerializedPKRelatedField
from netbox.api.serializers import NetBoxModelSerializer, NestedGroupModelSerializer, WritableNestedSerializer
from dcim.api.nested_serializers import NestedSiteSerializer
from netbox.constants import NESTED_SERIALIZER_PREFIX
from tenancy.api.nested_serializers import NestedTenantSerializer
from utilities.api import get_serializer_for_model

# from .field_serializers import IPAddressField
from .nested_serializers import *
from wim.choices import *
from wim.models import *



#
# Domains
#

class DomainSerializer(NestedGroupModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='wim-api:domain-detail')
    status = ChoiceField(
        choices=DomainStatusChoices,
        required=False,
    )
    asset_confidence = ChoiceField(
        choices=AssetConfidenceChoices,
        required=False,
    )
    # rir = NestedRIRSerializer()
    tenant = NestedTenantSerializer(required=False, allow_null=True)
    # asn_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Domain
        fields = (
            'id', 'url', 'display', 'name', 'status',
            'asset_confidence',
            'date_registrar_expiry', 'date_first_registered',
            'tenant',
        )


#
# FQDNs
#

class FQDNSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='wim-api:fqdn-detail')
    # -- Nested for FK Lookups --
    impacted_group_orig = NestedBusinessGroupSerializer(required=False, allow_null=True)
    impacted_division_orig = NestedBusinessDivisionSerializer(required=False, allow_null=True)
    vendor_company_fk = NestedVendorSerializer(required=False, allow_null=True)
    location = NestedSiteSerializer(required=False, allow_null=True)

    # -- M2M --
    software = SerializedPKRelatedField(
        queryset=Software.objects.all(),
        serializer=NestedSoftwareSerializer,
        required=False,
        many=True,
    )

    # -- Choices --
    status = ChoiceField(
        choices=FQDNStatusChoices,
        required=False,
    )
    fqdn_status = ChoiceField(
        choices=FQDNOpsStatusChoices,
        required=False,
        allow_blank=True,
    )
    website_status = ChoiceField(
        choices=WebsiteOpsStatusChoices,
        required=False,
        allow_blank=True,
    )
    tenant = NestedTenantSerializer(required=False, allow_null=True)
    # site = NestedSiteSerializer(required=False, allow_null=True)

    sitelocation_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = FQDN
        fields = (
            'id', 'url', 'display', 'name', 'status',
            'fqdn_status', 'website_status',
            'impacted_group_orig', 'impacted_division_orig',
            'software',
            'vendor_company_fk',
            'tenant', 'location',
            'sitelocation_count',
        )


#
# Brand
#

class BrandSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='wim-api:brand-detail')
    # tenant = NestedTenantSerializer(required=False, allow_null=True)

    class Meta:
        model = Brand
        fields = (
            'id', 'url', 'display', 'name',
        )


#
# BusinessGroup
#

class BusinessGroupSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='wim-api:businessgroup-detail')
    # status = ChoiceField(
    #     choices=FQDNStatusChoices,
    #     required=False,
    # )
    tenant = NestedTenantSerializer(required=False, allow_null=True)

    class Meta:
        model = BusinessGroup
        fields = (
            'id', 'url', 'display', 'name', 'acronym',
            'tenant',
        )


#
# BusinessDivision
#

class BusinessDivisionSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='wim-api:businessdivision-detail')
    # status = ChoiceField(
    #     choices=FQDNStatusChoices,
    #     required=False,
    # )
    tenant = NestedTenantSerializer(required=False, allow_null=True)

    class Meta:
        model = BusinessDivision
        fields = (
            'id', 'url', 'display', 'name', 'acronym',
            'tenant',
        )



#
# OperatingSystem
#

class OperatingSystemSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='wim-api:operatingsystem-detail')

    class Meta:
        model = OperatingSystem
        # TODO: Way to put __str__ in here? bc it concats the 3 fields that make up a full OS string
        fields = (
            'id', 'url', 'display', 'vendor', 'product', 'update',
            'platform_family', 'platform_type',
        )


#
# SiteLocation
#

class SiteLocationSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='wim-api:sitelocation-detail')
    # status = ChoiceField(
    #     choices=FQDNStatusChoices,
    #     required=False,
    # )
    # tenant = NestedTenantSerializer(required=False, allow_null=True)

    class Meta:
        model = SiteLocation
        fields = (
            'id', 'url', 'display', 'name', 'code',
        )


#
# Vendor
#

class VendorSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='wim-api:vendor-detail')
    # status = ChoiceField(
    #     choices=FQDNStatusChoices,
    #     required=False,
    # )
    # tenant = NestedTenantSerializer(required=False, allow_null=True)

    class Meta:
        model = Vendor
        fields = (
            'id', 'url', 'display', 'name',
        )



#
# WebEmail
#

class WebEmailSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='wim-api:webemail-detail')
    # status = ChoiceField(
    #     choices=FQDNStatusChoices,
    #     required=False,
    # )
    # tenant = NestedTenantSerializer(required=False, allow_null=True)

    class Meta:
        model = WebEmail
        fields = (
            'id', 'url', 'display', 'email_address',
        )



#
# Software
#

class SoftwareSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='wim-api:software-detail')
    # status = ChoiceField(
    #     choices=FQDNStatusChoices,
    #     required=False,
    # )
    # tenant = NestedTenantSerializer(required=False, allow_null=True)

    class Meta:
        model = Software
        fields = (
            'id', 'url', 'display', 'name', 'product', 'version', 'raw_banner', 'cpe'
        )
