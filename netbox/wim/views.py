from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch
# from django.db.models.expressions import RawSQL
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from circuits.models import Provider
from dcim.models import Interface, Site
from netbox.views import generic
# from tenancy.views import ObjectContactsView
from utilities.utils import count_related
from utilities.views import ViewTab, register_model_view

from . import filtersets, forms, tables
from .models import *


#
# -- Template Views List --
#
# - ListView, View, EditView, DeleteView, BulkImportView, BulkEditView, BulkDeleteView



#
# FQDNs
#

class FQDNListView(generic.ObjectListView):
    queryset = FQDN.objects.all()

    filterset = filtersets.FQDNFilterSet
    filterset_form = forms.FQDNFilterForm
    table = tables.FQDNTable


@register_model_view(FQDN)
class FQDNView(generic.ObjectView):
    queryset = FQDN.objects.all()


@register_model_view(FQDN, 'edit')
class FQDNEditView(generic.ObjectEditView):
    queryset = FQDN.objects.all()
    form = forms.FQDNForm


@register_model_view(FQDN, 'delete')
class FQDNDeleteView(generic.ObjectDeleteView):
    queryset = FQDN.objects.all()


class FQDNBulkImportView(generic.BulkImportView):
    queryset = FQDN.objects.all()
    model_form = forms.FQDNImportForm


class FQDNBulkEditView(generic.BulkEditView):
    queryset = FQDN.objects.all()
    filterset = filtersets.FQDNFilterSet
    table = tables.FQDNTable
    form = forms.FQDNBulkEditForm


class FQDNBulkDeleteView(generic.BulkDeleteView):
    queryset = FQDN.objects.all()
    # queryset = FQDN.objects.annotate(
    #     site_count=count_related(Site, 'fqdns')
    # )
    filterset = filtersets.FQDNFilterSet
    table = tables.FQDNTable




#
# Domains
#

class DomainListView(generic.ObjectListView):
    # queryset = Domain.objects.all()
    queryset = Domain.objects.annotate(
        fqdn_count=count_related(FQDN, 'domain'),
    )
    filterset = filtersets.DomainFilterSet
    filterset_form = forms.DomainFilterForm
    table = tables.DomainTable


@register_model_view(Domain)
class DomainView(generic.ObjectView):
    queryset = Domain.objects.all()

    def get_extra_context(self, request, instance):
        related_models = (
            (FQDN.objects.restrict(request.user, 'view').filter(domain=instance), 'domain_id'),
        )
        return {'related_models': related_models}


# TODO: Test this works later after we have data imported
# This view class sets up the tab that will show up if you click on a specific domain
# that will populate the tab with all related FQDNs
# @register_model_view(Domain, 'fqdns', path='fqdns')
# class DomainFQDNsView(generic.ObjectChildrenView):
#     queryset = Domain.objects.all()
#     child_model = FQDN
#     table = tables.FQDNTable
#     filterset = filtersets.FQDNFilterSet
#     template_name = 'wim/domain/fqdns.html'
#     # TODO: Need to define the badge properly with a count of related FQDNs
#     tab = ViewTab(
#         label=_('FQDNs'),
#         badge=lambda x: x.get_child_fqdns().count(),
#         permission='wim.view_fqdn',
#         weight=500,
#     )

#     def get_children(self, request, parent):
#         return parent.get_child_fqdns().restrict(request.user, 'view')


@register_model_view(Domain, 'edit')
class DomainEditView(generic.ObjectEditView):
    queryset = Domain.objects.all()
    form = forms.DomainForm


@register_model_view(Domain, 'delete')
class DomainDeleteView(generic.ObjectDeleteView):
    queryset = Domain.objects.all()


class DomainBulkImportView(generic.BulkImportView):
    queryset = Domain.objects.all()
    model_form = forms.DomainImportForm


class DomainBulkEditView(generic.BulkEditView):
    queryset = Domain.objects.all()
    # queryset = Domain.objects.annotate(
    #     site_count=count_related(Site, 'asns')
    # )
    filterset = filtersets.DomainFilterSet
    table = tables.DomainTable
    form = forms.DomainBulkEditForm


class DomainBulkDeleteView(generic.BulkDeleteView):
    queryset = Domain.objects.all()
    filterset = filtersets.DomainFilterSet
    table = tables.DomainTable



# --
# Brand
# --

class BrandListView(generic.ObjectListView):
    # queryset = Brand.objects.all()
    queryset = Brand.objects.annotate(
        # fqdn_count=count_related(FQDN, 'brand'),
        domain_count=count_related(Domain, 'brand'),
    )
    filterset = filtersets.BrandFilterSet
    filterset_form = forms.BrandFilterForm
    table = tables.BrandTable


@register_model_view(Brand)
class BrandView(generic.ObjectView):
    queryset = Brand.objects.all()

    def get_extra_context(self, request, instance):
        # TODO: The counts are working, but unsure how the links work yet
        related_models = (
            # (FQDN.objects.restrict(request.user, 'view').filter(brand=instance), 'brand_id'),
            (Domain.objects.restrict(request.user, 'view').filter(brand=instance), 'brand_id'),
        )
        return {'related_models': related_models}


@register_model_view(Brand, 'edit')
class BrandEditView(generic.ObjectEditView):
    queryset = Brand.objects.all()
    form = forms.BrandForm


@register_model_view(Brand, 'delete')
class BrandDeleteView(generic.ObjectDeleteView):
    queryset = Brand.objects.all()


class BrandBulkImportView(generic.BulkImportView):
    queryset = Brand.objects.all()
    model_form = forms.BrandImportForm


class BrandBulkEditView(generic.BulkEditView):
    queryset = Brand.objects.all()
    filterset = filtersets.BrandFilterSet
    table = tables.BrandTable
    form = forms.BrandBulkEditForm


class BrandBulkDeleteView(generic.BulkDeleteView):
    queryset = Brand.objects.all()
    filterset = filtersets.BrandFilterSet
    table = tables.BrandTable


# --
# Business Group
# --

class BusinessGroupListView(generic.ObjectListView):
    # queryset = BusinessGroup.objects.all()
    queryset = BusinessGroup.objects.annotate(
        fqdn_count=count_related(FQDN, 'impacted_group_orig'),
    )
    filterset = filtersets.BusinessGroupFilterSet
    filterset_form = forms.BusinessGroupFilterForm
    table = tables.BusinessGroupTable


@register_model_view(BusinessGroup)
class BusinessGroupView(generic.ObjectView):
    queryset = BusinessGroup.objects.all()

    def get_extra_context(self, request, instance):
        # TODO: The counts are working, but unsure how the links work yet
        related_models = (
            (FQDN.objects.restrict(request.user, 'view').filter(impacted_group_orig=instance), 'businessgroup_id'),
            (BusinessDivision.objects.restrict(request.user, 'view').filter(group=instance), 'businessgroup_id'),
        )
        return {'related_models': related_models}


@register_model_view(BusinessGroup, 'edit')
class BusinessGroupEditView(generic.ObjectEditView):
    queryset = BusinessGroup.objects.all()
    form = forms.BusinessGroupForm


@register_model_view(BusinessGroup, 'delete')
class BusinessGroupDeleteView(generic.ObjectDeleteView):
    queryset = BusinessGroup.objects.all()


class BusinessGroupBulkImportView(generic.BulkImportView):
    queryset = BusinessGroup.objects.all()
    model_form = forms.BusinessGroupImportForm


class BusinessGroupBulkEditView(generic.BulkEditView):
    queryset = BusinessGroup.objects.all()
    filterset = filtersets.BusinessGroupFilterSet
    table = tables.BusinessGroupTable
    form = forms.BusinessGroupBulkEditForm


class BusinessGroupBulkDeleteView(generic.BulkDeleteView):
    queryset = BusinessGroup.objects.all()
    filterset = filtersets.BusinessGroupFilterSet
    table = tables.BusinessGroupTable



# --
# Business Division
# --

class BusinessDivisionListView(generic.ObjectListView):
    # queryset = BusinessDivision.objects.all()
    queryset = BusinessDivision.objects.annotate(
        fqdn_count=count_related(FQDN, 'impacted_division_orig'),
    )
    filterset = filtersets.BusinessDivisionFilterSet
    filterset_form = forms.BusinessDivisionFilterForm
    table = tables.BusinessDivisionTable


@register_model_view(BusinessDivision)
class BusinessDivisionView(generic.ObjectView):
    queryset = BusinessDivision.objects.all()

    def get_extra_context(self, request, instance):
        related_models = (
            (FQDN.objects.restrict(request.user, 'view').filter(impacted_division_orig=instance), 'businessdivision_id'),
        )
        return {'related_models': related_models}


@register_model_view(BusinessDivision, 'edit')
class BusinessDivisionEditView(generic.ObjectEditView):
    queryset = BusinessDivision.objects.all()
    form = forms.BusinessDivisionForm


@register_model_view(BusinessDivision, 'delete')
class BusinessDivisionDeleteView(generic.ObjectDeleteView):
    queryset = BusinessDivision.objects.all()


class BusinessDivisionBulkImportView(generic.BulkImportView):
    queryset = BusinessDivision.objects.all()
    model_form = forms.BusinessDivisionImportForm


class BusinessDivisionBulkEditView(generic.BulkEditView):
    queryset = BusinessDivision.objects.all()
    filterset = filtersets.BusinessDivisionFilterSet
    table = tables.BusinessDivisionTable
    form = forms.BusinessDivisionBulkEditForm


class BusinessDivisionBulkDeleteView(generic.BulkDeleteView):
    queryset = BusinessDivision.objects.all()
    filterset = filtersets.BusinessDivisionFilterSet
    table = tables.BusinessDivisionTable



# --
# Operating Systems
# --

class OperatingSystemListView(generic.ObjectListView):
    # queryset = OperatingSystem.objects.all()
    queryset = OperatingSystem.objects.annotate(
        fqdn_count=count_related(FQDN, 'os_1')
    )
    filterset = filtersets.OperatingSystemFilterSet
    filterset_form = forms.OperatingSystemFilterForm
    table = tables.OperatingSystemTable


@register_model_view(OperatingSystem)
class OperatingSystemView(generic.ObjectView):
    queryset = OperatingSystem.objects.all()

    def get_extra_context(self, request, instance):
        related_models = (
            (FQDN.objects.restrict(request.user, 'view').filter(os_1=instance), 'os_1_id'),
        )
        return {'related_models': related_models}


@register_model_view(OperatingSystem, 'edit')
class OperatingSystemEditView(generic.ObjectEditView):
    queryset = OperatingSystem.objects.all()
    form = forms.OperatingSystemForm


@register_model_view(OperatingSystem, 'delete')
class OperatingSystemDeleteView(generic.ObjectDeleteView):
    queryset = OperatingSystem.objects.all()


class OperatingSystemBulkImportView(generic.BulkImportView):
    queryset = OperatingSystem.objects.all()
    model_form = forms.OperatingSystemImportForm


class OperatingSystemBulkEditView(generic.BulkEditView):
    queryset = OperatingSystem.objects.all()
    filterset = filtersets.OperatingSystemFilterSet
    table = tables.OperatingSystemTable
    form = forms.OperatingSystemBulkEditForm


class OperatingSystemBulkDeleteView(generic.BulkDeleteView):
    queryset = OperatingSystem.objects.all()
    filterset = filtersets.OperatingSystemFilterSet
    table = tables.OperatingSystemTable



# --
# SiteLocation
# --

class SiteLocationListView(generic.ObjectListView):
    # queryset = SiteLocation.objects.all()
    queryset = SiteLocation.objects.annotate(
        fqdn_count=count_related(FQDN, 'location_orig')
    )
    filterset = filtersets.SiteLocationFilterSet
    filterset_form = forms.SiteLocationFilterForm
    table = tables.SiteLocationTable


@register_model_view(SiteLocation)
class SiteLocationView(generic.ObjectView):
    queryset = SiteLocation.objects.all()

    def get_extra_context(self, request, instance):
        related_models = (
            (FQDN.objects.restrict(request.user, 'view').filter(location_orig=instance), 'location_orig_id'),
        )
        return {'related_models': related_models}


@register_model_view(SiteLocation, 'edit')
class SiteLocationEditView(generic.ObjectEditView):
    queryset = SiteLocation.objects.all()
    form = forms.SiteLocationForm


@register_model_view(SiteLocation, 'delete')
class SiteLocationDeleteView(generic.ObjectDeleteView):
    queryset = SiteLocation.objects.all()


class SiteLocationBulkImportView(generic.BulkImportView):
    queryset = SiteLocation.objects.all()
    model_form = forms.SiteLocationImportForm


class SiteLocationBulkEditView(generic.BulkEditView):
    queryset = SiteLocation.objects.all()
    filterset = filtersets.SiteLocationFilterSet
    table = tables.SiteLocationTable
    form = forms.SiteLocationBulkEditForm


class SiteLocationBulkDeleteView(generic.BulkDeleteView):
    queryset = SiteLocation.objects.all()
    filterset = filtersets.SiteLocationFilterSet
    table = tables.SiteLocationTable




# --
# Vendor
# --

class VendorListView(generic.ObjectListView):
    # queryset = Vendor.objects.all()
    queryset = Vendor.objects.annotate(
        fqdn_count=count_related(FQDN, 'vendor_company_fk')
    )
    filterset = filtersets.VendorFilterSet
    filterset_form = forms.VendorFilterForm
    table = tables.VendorTable


@register_model_view(Vendor)
class VendorView(generic.ObjectView):
    queryset = Vendor.objects.all()

    def get_extra_context(self, request, instance):
        related_models = (
            (FQDN.objects.restrict(request.user, 'view').filter(vendor_company_fk=instance), 'vendor_id'),
        )
        return {"related_models": related_models}


@register_model_view(Vendor, 'edit')
class VendorEditView(generic.ObjectEditView):
    queryset = Vendor.objects.all()
    form = forms.VendorForm


@register_model_view(Vendor, 'delete')
class VendorDeleteView(generic.ObjectDeleteView):
    queryset = Vendor.objects.all()


class VendorBulkImportView(generic.BulkImportView):
    queryset = Vendor.objects.all()
    model_form = forms.VendorImportForm


class VendorBulkEditView(generic.BulkEditView):
    queryset = Vendor.objects.all()
    filterset = filtersets.VendorFilterSet
    table = tables.VendorTable
    form = forms.VendorBulkEditForm


class VendorBulkDeleteView(generic.BulkDeleteView):
    queryset = Vendor.objects.all()
    filterset = filtersets.VendorFilterSet
    table = tables.VendorTable





# --
# WebEmail
# --

class WebEmailListView(generic.ObjectListView):
    queryset = WebEmail.objects.all()
    filterset = filtersets.WebEmailFilterSet
    filterset_form = forms.WebEmailFilterForm
    table = tables.WebEmailTable


# @register_model_view(WebEmail)
# class WebEmailView(generic.ObjectView):
#     queryset = WebEmail.objects.all()


# @register_model_view(WebEmail, 'edit')
# class WebEmailEditView(generic.ObjectEditView):
#     queryset = WebEmail.objects.all()
#     form = forms.WebEmailForm


# @register_model_view(WebEmail, 'delete')
# class WebEmailDeleteView(generic.ObjectDeleteView):
#     queryset = WebEmail.objects.all()


# class WebEmailBulkImportView(generic.BulkImportView):
#     queryset = WebEmail.objects.all()
#     model_form = forms.WebEmailImportForm


# class WebEmailBulkEditView(generic.BulkEditView):
#     queryset = WebEmail.objects.all()
#     filterset = filtersets.WebEmailFilterSet
#     table = tables.WebEmailTable
#     form = forms.WebEmailBulkEditForm


# class WebEmailBulkDeleteView(generic.BulkDeleteView):
#     queryset = WebEmail.objects.all()
#     filterset = filtersets.WebEmailFilterSet
#     table = tables.WebEmailTable



# --
# Software
# --

class SoftwareListView(generic.ObjectListView):
    # queryset = Software.objects.all()
    queryset = Software.objects.annotate(
        fqdn_count=count_related(FQDN, 'software')
    )
    filterset = filtersets.SoftwareFilterSet
    filterset_form = forms.SoftwareFilterForm
    table = tables.SoftwareTable


@register_model_view(Software)
class SoftwareView(generic.ObjectView):
    queryset = Software.objects.all()

    def get_extra_context(self, request, instance):
        related_models = (
            (FQDN.objects.restrict(request.user, 'view').filter(software__in=[instance]), 'software_id'),
        )
        return {'related_models': related_models}


@register_model_view(Software, 'edit')
class SoftwareEditView(generic.ObjectEditView):
    queryset = Software.objects.all()
    form = forms.SoftwareForm


@register_model_view(Software, 'delete')
class SoftwareDeleteView(generic.ObjectDeleteView):
    queryset = Software.objects.all()


class SoftwareBulkImportView(generic.BulkImportView):
    queryset = Software.objects.all()
    model_form = forms.SoftwareImportForm


class SoftwareBulkEditView(generic.BulkEditView):
    queryset = Software.objects.all()
    filterset = filtersets.SoftwareFilterSet
    table = tables.SoftwareTable
    form = forms.SoftwareBulkEditForm


class SoftwareBulkDeleteView(generic.BulkDeleteView):
    queryset = Software.objects.all()
    filterset = filtersets.SoftwareFilterSet
    table = tables.SoftwareTable



# --
# Action Views
# --

# Registering the /scan/ path for a domain
# register_model_view(
#     Domain,
#     'scan',
#     kwargs={'model': Domain}
# )

@register_model_view(Domain, 'scan')
class DomainScanView(generic.ObjectView):
    """
    Run a domain enumeration scan and display the results.
    NOTE: See dcim.views.py -> PathTraceView() for example of doing this
    """
    pass
    # additional_permissions = ['wim.view_scans']
    # template_name = "wim/scan/domain_scan.html"

    queryset = Domain.objects.all()

    # def dispatch(self, request, *args, **kwargs):
    #     model = kwargs.pop('model')
    #     self.queryset = Domain.objects.all()
    #     return super().dispatch(request, *args, **kwargs)

    # TODO: My goal is to maybe send this to a job/task, and
    # send user back to the return_url path for now.
    # They can go pull up the job results later.
    # Otherwise, the job will run, finish, and automatically update
    # our dataset with the results of the scan, without requiring user to
    # review it or do anything other than push the scan button from the start.



@register_model_view(FQDN, 'scan')
class FQDNScanView(generic.ObjectView):
    """
    Run a domain enumeration scan and display the results.
    NOTE: See dcim.views.py -> PathTraceView() for example of doing this
    """
    pass
    # additional_permissions = ['wim.view_scans']
    # template_name = "wim/scan/domain_scan.html"

    queryset = FQDN.objects.all()
