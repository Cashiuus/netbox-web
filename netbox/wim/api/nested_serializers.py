
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from netbox.api.serializers import WritableNestedSerializer
from wim import models



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
