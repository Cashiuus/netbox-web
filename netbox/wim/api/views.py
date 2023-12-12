# from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
# from django.db import transaction
# from django.shortcuts import get_object_or_404
# from django_pglocks import advisory_lock
# from drf_spectacular.utils import extend_schema
# from rest_framework import status
# from rest_framework.response import Response
from rest_framework.routers import APIRootView
# from rest_framework.views import APIView

# from circuits.models import Provider
# from dcim.models import Site
# from ipam import filtersets
# from ipam.models import *
from netbox.api.viewsets import NetBoxModelViewSet
# from netbox.api.viewsets.mixins import ObjectValidationMixin
from netbox.config import get_config
# from netbox.constants import ADVISORY_LOCK_KEYS
from utilities.utils import count_related

from wim import filtersets
from wim.models import *
from wim.api import serializers


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
class BrandViewSet(NetBoxModelViewSet):
    queryset = Brand.objects.prefetch_related('tags').annotate(
        # fqdn_count=count_related(FQDN, 'brand'),
        domain_count=count_related(Domain, 'brand')
    )
    serializer_class = serializers.BrandSerializer
    filterset_class = filtersets.BrandFilterSet


class BusinessGroupViewSet(NetBoxModelViewSet):
    queryset = BusinessGroup.objects.prefetch_related('tags').annotate(
        fqdn_count=count_related(FQDN, 'impacted_group_orig')
    )
    serializer_class = serializers.BusinessGroupSerializer
    filterset_class = filtersets.BusinessGroupFilterSet


class BusinessDivisionViewSet(NetBoxModelViewSet):
    queryset = BusinessDivision.objects.prefetch_related('tags').annotate(
        fqdn_count=count_related(FQDN, 'impacted_division_orig')
    )
    serializer_class = serializers.BusinessDivisionSerializer
    filterset_class = filtersets.BusinessDivisionFilterSet


class CertificateViewSet(NetBoxModelViewSet):
    # queryset = Certificate.objects.all()
    queryset = Certificate.objects.prefetch_related('tags').annotate(
        fqdn_count=count_related(FQDN, 'certificate')
    )
    serializer_class = serializers.CertificateSerializer
    filterset_class = filtersets.CertificateFilterSet


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
        'impacted_group_orig', 'impacted_division_orig', 'domain',
        'vendor_company_fk', 'software', 'location_orig', 'location',
        'certificate',
        'tags',
    )
    serializer_class = serializers.FQDNSerializer
    filterset_class = filtersets.FQDNFilterSet


class OperatingSystemViewSet(NetBoxModelViewSet):
    queryset = OperatingSystem.objects.prefetch_related('tags').annotate(
        fqdn_count=count_related(FQDN, 'os_1')
    )
    serializer_class = serializers.OperatingSystemSerializer
    filterset_class = filtersets.OperatingSystemFilterSet


class SiteLocationViewSet(NetBoxModelViewSet):
    queryset = SiteLocation.objects.prefetch_related('tags')
    serializer_class = serializers.SiteLocationSerializer
    filterset_class = filtersets.SiteLocationFilterSet


class SoftwareViewSet(NetBoxModelViewSet):
    # NOTE: This queryset points to FQDN, therefore uses the fieldname
    # that is defined there for the software M2M model field
    queryset = Software.objects.annotate(
        fqdn_count=count_related(FQDN, 'software')
    )
    serializer_class = serializers.SoftwareSerializer
    filterset_class = filtersets.SoftwareFilterSet


class VendorViewSet(NetBoxModelViewSet):
    queryset = Vendor.objects.prefetch_related('tags').annotate(
        fqdn_count=count_related(FQDN, 'vendor_company_fk')
    )
    serializer_class = serializers.VendorSerializer
    filterset_class = filtersets.VendorFilterSet


class WebEmailViewSet(NetBoxModelViewSet):
    queryset = WebEmail.objects.annotate(
        # For WebEmail, its related_name = "domains"
        # Its ManyToManyField FK fieldname in Domains table is "registration_emails"
        fqdn_count=count_related(Domain, 'registration_emails')
    )
    serializer_class = serializers.WebEmailSerializer
    filterset_class = filtersets.WebEmailFilterSet
