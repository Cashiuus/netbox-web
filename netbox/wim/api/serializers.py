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
    tenant = NestedTenantSerializer(required=False, allow_null=True)

    class Meta:
        model = FQDN
        fields = (
            'id', 'url', 'name', 'status',
            'fqdn_status', 'website_status',
            'tenant',
        )
