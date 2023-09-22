
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from netbox.api.serializers import WritableNestedSerializer
from wim import models


class NestedDomainSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='wim-api:domain-detail')

    class Meta:
        model = models.Domain
        fields = ['id', 'url', 'display', 'name']


class NestedFQDNSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='wim-api:fqdn-detail')

    class Meta:
        model = models.FQDN
        fields = ['id', 'url', 'display', 'name']


class NestedBrandSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='wim-api:brand-detail')

    class Meta:
        model = models.Brand
        fields = ('id', 'url', 'display', 'name', 'slug')


class NestedBusinessGroupSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='wim-api:businessgroup-detail')

    class Meta:
        model = models.BusinessGroup
        fields = ('id', 'url', 'display', 'name', 'slug', 'acronym')


class NestedBusinessDivisionSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='wim-api:businessdivision-detail')

    class Meta:
        model = models.BusinessDivision
        fields = ('id', 'url', 'display', 'name', 'slug', 'acronym')


@extend_schema_serializer(
    exclude_fields=('fqdn_count',)
)
class NestedVendorSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='wim-api:vendor-detail')
    fqdn_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Vendor
        fields = ('id', 'url', 'display', 'name', 'slug', 'fqdn_count')
