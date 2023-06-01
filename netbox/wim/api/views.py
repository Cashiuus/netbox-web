from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404
from django_pglocks import advisory_lock
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.routers import APIRootView
from rest_framework.views import APIView

# from circuits.models import Provider
from dcim.models import Site
# from ipam import filtersets
# from ipam.models import *
from netbox.api.viewsets import NetBoxModelViewSet
from netbox.api.viewsets.mixins import ObjectValidationMixin
from netbox.config import get_config
# from netbox.constants import ADVISORY_LOCK_KEYS
from utilities.utils import count_related
from . import serializers
from wim import filtersets
from wim.models import *


class WIMRootView(APIRootView):
    """
    WIM API Root View
    """
    def get_view_name(self):
        return "WIM"


# -- Mixins Go Here --




# 
# Model ViewSets
#

class DomainViewSet(NetBoxModelViewSet):
    # This method came from ipam/api/views.py
    # queryset = Domain.objects.prefetch_related(
    #     'tenant', 'registrar_company', 'tags',
    # )
    # This method came from dcim/api/views.py
    # queryset = Domain.objects.add_related_count(
    #     Domain.objects.all(),
    #     FQDN,
    #     'domain',
    #     'fdn_count',
    #     cumulative=True,
    # ).prefetch_related('tags')

    # Test with just objects
    queryset = Domain.objects.all()

    serializer_class = serializers.DomainSerializer
    filterset_class = filtersets.DomainFilterSet


class FQDNViewSet(NetBoxModelViewSet):
    queryset = FQDN.objects.prefetch_related(
        'tenant', 'impacted_business_9', 'impacted_division_9', 'domain',
        'tags',
    )
    serializer_class = serializers.FQDNSerializer
    filterset_class = filtersets.FQDNFilterSet



# class VendorViewSet(NetBoxModelViewSet):
#     queryset = Vendor.objects.prefetch_related('tags').
#     annotate(
#         fqdn_count=count_related(FQDN, 'vendor')
#     )
#     serializer_class = serializers.VendorSerializer
#     filterset_class = filtersets.VendorFilterSet
