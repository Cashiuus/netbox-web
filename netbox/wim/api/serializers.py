from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from dcim.api.nested_serializers import NestedDeviceSerializer, NestedSiteSerializer
# from ipam.choices import *
# from ipam.constants import IPADDRESS_ASSIGNMENT_MODELS, VLANGROUP_SCOPE_TYPES
# from ipam.models import *
from netbox.api.fields import ChoiceField, ContentTypeField, SerializedPKRelatedField
from netbox.api.serializers import NetBoxModelSerializer
from netbox.constants import NESTED_SERIALIZER_PREFIX
from tenancy.api.nested_serializers import NestedTenantSerializer
from utilities.api import get_serializer_for_model
from virtualization.api.nested_serializers import NestedVirtualMachineSerializer

# from .nested_serializers import *
# from .field_serializers import IPAddressField

from wim.choices import *
from wim.models import *



#
# Domains
#

class DomainSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='wim-api:domain-detail')
    # rir = NestedRIRSerializer()
    tenant = NestedTenantSerializer(required=False, allow_null=True)
    # asn_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Domain
        fields = [
            'id', 'name', 'date_registrar_expiry', 'date_first_registered',
        ]


#
# FQDNs
#

class FQDNSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='wim-api:fqdn-detail')
    # rir = NestedRIRSerializer()
    tenant = NestedTenantSerializer(required=False, allow_null=True)
    # asn_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = FQDN
        fields = [
            'id', 'name', 'status', 'fqdn_status', 'website_status',
        ]
