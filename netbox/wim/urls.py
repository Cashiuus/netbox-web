from django.urls import include, path

from utilities.urls import get_model_urls
from . import views

app_name = 'wim'

urlpatterns = [
    # FQDN's
    path('fqdns/', views.FQDNListView.as_view(), name='fqdn_list'),
    path('fqdns/add/', views.FQDNEditView.as_view(), name='fqdn_add'),
    path('fqdns/import/', views.FQDNBulkImportView.as_view(), name='fqdn_import'),
    path('fqdns/edit/', views.FQDNBulkEditView.as_view(), name='fqdn_bulk_edit'),
    path('fqdns/delete/', views.FQDNBulkDeleteView.as_view(), name='fqdn_bulk_delete'),
    path('fqdns/<int:pk>/', include(get_model_urls('wim', 'fqdn'))),

    # Domain Roots
    path('domains/', views.DomainListView.as_view(), name='domain_list'),
    path('domains/add/', views.DomainEditView.as_view(), name='domain_add'),
    path('domains/import/', views.DomainBulkImportView.as_view(), name='domain_import'),
    path('domains/edit/', views.DomainBulkEditView.as_view(), name='domain_bulk_edit'),
    path('domains/delete/', views.DomainBulkDeleteView.as_view(), name='domain_bulk_delete'),
    path('domains/<int:pk>/', include(get_model_urls('wim', 'domain'))),
]