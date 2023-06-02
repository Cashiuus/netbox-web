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
    # queryset = FQDN.objects.annotate(
        # site_count=count_related(Site, 'asns'),
        # provider_count=count_related(Provider, 'asns')
    # )
    filterset = filtersets.FQDNFilterSet
    filterset_form = forms.FQDNFilterForm
    table = tables.FQDNTable


@register_model_view(FQDN)
class FQDNView(generic.ObjectView):
    queryset = FQDN.objects.all()

    # def get_extra_context(self, request, instance):
    #     related_models = (
    #         (Site.objects.restrict(request.user, 'view').filter(fqdn__in=[instance]), 'name'),
    #         # (Provider.objects.restrict(request.user, 'view').filter(asns__in=[instance]), 'id'),
    #     )
    #     return {
    #         'related_models': related_models,
    #     }


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
    # queryset = FQDN.objects.annotate(
    #     site_count=count_related(Site, 'fqdns')
    # )
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
    queryset = Domain.objects.all()
    # queryset = Domain.objects.annotate(
    #     site_count=count_related(Site, 'domains'),
    #     # provider_count=count_related(Provider, 'asns')
    # )
    filterset = filtersets.DomainFilterSet
    filterset_form = forms.DomainFilterForm
    table = tables.DomainTable


@register_model_view(Domain)
class DomainView(generic.ObjectView):
    queryset = Domain.objects.all()

    # def get_extra_context(self, request, instance):
    #     related_models = (
    #         (Registrar.objects.restrict(request.user, 'view').filter(domains__in=[instance]), 'id'),
    #         (FQDN.objects.restrict(request.user, 'view').filter(domains__in=[instance]), 'id'),
    #         # (Site.objects.restrict(request.user, 'view').filter(asns__in=[instance]), 'id'),
    #         # (Provider.objects.restrict(request.user, 'view').filter(asns__in=[instance]), 'id'),
    #     )

    #     return {
    #         'related_models': related_models,
    #     }

# TODO: Test this works later after we have data imported
# This view class sets up the tab that will show up if you click on a specific domain
# that will populate the tab with all related FQDNs
# @register_model_view(Domain, 'fqdns', path='domain-fqdns')
# class DomainFQDNsView(generic.ObjectChildrenView):
#     queryset = Domain.objects.all()
#     child_model = FQDN
#     table = tables.FQDNTable
#     filterset = filtersets.FQDNFilterSet
#     template_name = 'wim/domain/domain_fqdns.html'
#     # TODO: Need to define the badge properly with a count of related FQDNs
#     tab = ViewTab(
#         label=_('FQDNs'),
#         badge=lambda x: x.get_child_fqdns().count(),
#         permission='wim.view_fqdns',
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
    # queryset = Domain.objects.annotate(
    #     site_count=count_related(Site, 'asns')
    # )
    filterset = filtersets.DomainFilterSet
    table = tables.DomainTable




# --
# Business Group
# --

class BusinessGroupListView(generic.ObjectListView):
    queryset = BusinessGroup.objects.all()
    filterset = filtersets.BusinessGroupFilterSet
    filterset_form = forms.BusinessGroupFilterForm
    table = tables.BusinessGroupTable


@register_model_view(BusinessGroup)
class BusinessGroupView(generic.ObjectView):
    queryset = BusinessGroup.objects.all()


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
    queryset = BusinessDivision.objects.all()
    filterset = filtersets.BusinessDivisionFilterSet
    filterset_form = forms.BusinessDivisionFilterForm
    table = tables.BusinessDivisionTable


@register_model_view(BusinessDivision)
class BusinessDivisionView(generic.ObjectView):
    queryset = BusinessDivision.objects.all()
    

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


class BusinessGroupBulkDeleteView(generic.BulkDeleteView):
    queryset = BusinessDivision.objects.all()
    filterset = filtersets.BusinessDivisionFilterSet
    table = tables.BusinessDivisionTable





# --
# Operating Systems
# --

class OperatingSystemListView(generic.ObjectListView):
    queryset = OperatingSystem.objects.all()
    filterset = filtersets.OperatingSystemFilterSet
    filterset_form = forms.OperatingSystemFilterForm
    table = tables.OperatingSystemTable


@register_model_view(OperatingSystem)
class OperatingSystemView(generic.ObjectView):
    queryset = OperatingSystem.objects.all()
    

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






# # --
# # Registrar
# # --

# class RegistrarListView(generic.ObjectListView):
#     queryset = Registrar.objects.all()
#     filterset = filtersets.RegistrarFilterSet
#     filterset_form = forms.RegistrarFilterForm
#     table = tables.OperatingSystemTable


# @register_model_view(OperatingSystem)
# class OperatingSystemView(generic.ObjectView):
#     queryset = OperatingSystem.objects.all()
    

# @register_model_view(OperatingSystem, 'edit')
# class OperatingSystemEditView(generic.ObjectEditView):
#     queryset = OperatingSystem.objects.all()
#     form = forms.OperatingSystemForm


# @register_model_view(OperatingSystem, 'delete')
# class OperatingSystemDeleteView(generic.ObjectDeleteView):
#     queryset = OperatingSystem.objects.all()


# class OperatingSystemBulkImportView(generic.BulkImportView):
#     queryset = OperatingSystem.objects.all()
#     model_form = forms.OperatingSystemImportForm


# class OperatingSystemBulkEditView(generic.BulkEditView):
#     queryset = OperatingSystem.objects.all()
#     filterset = filtersets.OperatingSystemFilterSet
#     table = tables.OperatingSystemTable
#     form = forms.OperatingSystemBulkEditForm


# class OperatingSystemBulkDeleteView(generic.BulkDeleteView):
#     queryset = OperatingSystem.objects.all()
#     filterset = filtersets.OperatingSystemFilterSet
#     table = tables.OperatingSystemTable


