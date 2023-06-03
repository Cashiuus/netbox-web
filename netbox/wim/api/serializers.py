# from django.contrib.contenttypes.models import ContentType
# from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from netbox.api.fields import ChoiceField, ContentTypeField, SerializedPKRelatedField
from netbox.api.serializers import NetBoxModelSerializer, NestedGroupModelSerializer, WritableNestedSerializer
from netbox.constants import NESTED_SERIALIZER_PREFIX
from tenancy.api.nested_serializers import NestedTenantSerializer
from utilities.api import get_serializer_for_model

# from .nested_serializers import *
# from .field_serializers import IPAddressField

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
    # rir = NestedRIRSerializer()
    tenant = NestedTenantSerializer(required=False, allow_null=True)
    # asn_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Domain
        fields = (
            'id', 'url', 'name', 'status',
            'date_registrar_expiry', 'date_first_registered',
            'tenant',
        )


#
# FQDNs
#

class FQDNSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='wim-api:fqdn-detail')
    status = ChoiceField(
        choices=FQDNStatusChoices,
        required=False,
    )
    fqdn_status = ChoiceField(
        choices=FQDNOpsStatusChoices,
        required=False,
    )
    website_status = ChoiceField(
        choices=WebsiteOpsStatusChoices,
        required=False,
    )
    tenant = NestedTenantSerializer(required=False, allow_null=True)

    class Meta:
        model = FQDN
        fields = (
            'id', 'url', 'name', 'status',
            'fqdn_status', 'website_status',
            'tenant',
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
            'id', 'url', 'name',
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
            'id', 'url', 'name',
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
            'id', 'url', 'vendor', 'product', 'update', 'family'
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
            'id', 'url', 'name', 'code',
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
            'id', 'url', 'name',
        )



#
# WebserverFramework
#

class WebserverFrameworkSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='wim-api:webserverframework-detail')
    # status = ChoiceField(
    #     choices=FQDNStatusChoices,
    #     required=False,
    # )
    # tenant = NestedTenantSerializer(required=False, allow_null=True)

    class Meta:
        model = WebserverFramework
        fields = (
            'id', 'url', 'name', 'product', 'version', 'raw_banner', 'cpe'
        )

