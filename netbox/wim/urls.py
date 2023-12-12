from django.urls import include, path
from utilities.urls import get_model_urls
from . import views

app_name = 'wim'

urlpatterns = [
    # FQDN's
    path('fqdns/', views.FQDNListView.as_view(), name='fqdn_list'),
    path('fqdns/default', views.FQDNDefaultFilteredListView.as_view(), name='fqdn_list_filtered'),
    path('fqdns/add/', views.FQDNEditView.as_view(), name='fqdn_add'),
    path('fqdns/import/', views.FQDNBulkImportView.as_view(), name='fqdn_import'),
    path('fqdns/edit/', views.FQDNBulkEditView.as_view(), name='fqdn_bulk_edit'),
    path('fqdns/delete/', views.FQDNBulkDeleteView.as_view(), name='fqdn_bulk_delete'),
    # NOTE: Because '/scan/' is a model view like the others, it should fall under this inclusion
    path('fqdns/<int:pk>/', include(get_model_urls('wim', 'fqdn'))),

    # Domain Roots
    path('domains/', views.DomainListView.as_view(), name='domain_list'),
    path('domains/add/', views.DomainEditView.as_view(), name='domain_add'),
    path('domains/import/', views.DomainBulkImportView.as_view(), name='domain_import'),
    path('domains/edit/', views.DomainBulkEditView.as_view(), name='domain_bulk_edit'),
    path('domains/delete/', views.DomainBulkDeleteView.as_view(), name='domain_bulk_delete'),
    path('domains/<int:pk>/', include(get_model_urls('wim', 'domain'))),

    # Certificates (TLS/Encryption web certificates)
    path('certificates/', views.CertificateListView.as_view(), name='certificate_list'),
    path('certificates/add/', views.CertificateEditView.as_view(), name='certificate_add'),
    path('certificates/import/', views.CertificateBulkImportView.as_view(), name='certificate_import'),
    path('certificates/edit/', views.CertificateBulkEditView.as_view(), name='certificate_bulk_edit'),
    path('certificates/delete/', views.CertificateBulkDeleteView.as_view(), name='certificate_bulk_delete'),
    path('certificates/<int:pk>/', include(get_model_urls('wim', 'certificate'))),

    # Brands
    path('brands/', views.BrandListView.as_view(), name='brand_list'),
    path('brands/add/', views.BrandEditView.as_view(), name='brand_add'),
    path('brands/import/', views.BrandBulkImportView.as_view(), name='brand_import'),
    path('brands/edit/', views.BrandBulkEditView.as_view(), name='brand_bulk_edit'),
    path('brands/delete/', views.BrandBulkDeleteView.as_view(), name='brand_bulk_delete'),
    path('brands/<int:pk>/', include(get_model_urls('wim', 'brand'))),

    # Business Groups
    path('business-groups/', views.BusinessGroupListView.as_view(), name='businessgroup_list'),
    path('business-groups/add/', views.BusinessGroupEditView.as_view(), name='businessgroup_add'),
    path('business-groups/import/', views.BusinessGroupBulkImportView.as_view(), name='businessgroup_import'),
    path('business-groups/edit/', views.BusinessGroupBulkEditView.as_view(), name='businessgroup_bulk_edit'),
    path('business-groups/delete/', views.BusinessGroupBulkDeleteView.as_view(), name='businessgroup_bulk_delete'),
    path('business-groups/<int:pk>/', include(get_model_urls('wim', 'businessgroup'))),

    # Business Divisions
    path('business-divisions/', views.BusinessDivisionListView.as_view(), name='businessdivision_list'),
    path('business-divisions/add/', views.BusinessDivisionEditView.as_view(), name='businessdivision_add'),
    path('business-divisions/import/', views.BusinessDivisionBulkImportView.as_view(), name='businessdivision_import'),
    path('business-divisions/edit/', views.BusinessDivisionBulkEditView.as_view(), name='businessdivision_bulk_edit'),
    path('business-divisions/delete/', views.BusinessDivisionBulkDeleteView.as_view(), name='businessdivision_bulk_delete'),
    path('business-divisions/<int:pk>/', include(get_model_urls('wim', 'businessdivision'))),

    # Operating Systems
    path('os/', views.OperatingSystemListView.as_view(), name='operatingsystem_list'),
    path('os/add/', views.OperatingSystemEditView.as_view(), name='operatingsystem_add'),
    path('os/import/', views.OperatingSystemBulkImportView.as_view(), name='operatingsystem_import'),
    path('os/edit/', views.OperatingSystemBulkEditView.as_view(), name='operatingsystem_bulk_edit'),
    path('os/delete/', views.OperatingSystemBulkDeleteView.as_view(), name='operatingsystem_bulk_delete'),
    path('os/<int:pk>/', include(get_model_urls('wim', 'operatingsystem'))),

    # Site Locations
    path('site-locations/', views.SiteLocationListView.as_view(), name='sitelocation_list'),
    path('site-locations/add/', views.SiteLocationEditView.as_view(), name='sitelocation_add'),
    path('site-locations/import/', views.SiteLocationBulkImportView.as_view(), name='sitelocation_import'),
    path('site-locations/edit/', views.SiteLocationBulkEditView.as_view(), name='sitelocation_bulk_edit'),
    path('site-locations/delete/', views.SiteLocationBulkDeleteView.as_view(), name='sitelocation_bulk_delete'),
    path('site-locations/<int:pk>/', include(get_model_urls('wim', 'sitelocation'))),

    # Vendors
    path('vendors/', views.VendorListView.as_view(), name='vendor_list'),
    path('vendors/add/', views.VendorEditView.as_view(), name='vendor_add'),
    path('vendors/import/', views.VendorBulkImportView.as_view(), name='vendor_import'),
    path('vendors/edit/', views.VendorBulkEditView.as_view(), name='vendor_bulk_edit'),
    path('vendors/delete/', views.VendorBulkDeleteView.as_view(), name='vendor_bulk_delete'),
    path('vendors/<int:pk>/', include(get_model_urls('wim', 'vendor'))),

    # Web Emails
    path('web-emails/', views.WebEmailListView.as_view(), name='webemail_list'),
    # path('web-emails/add/', views.WebEmailEditView.as_view(), name='webemail_add'),
    # path('web-emails/import/', views.WebEmailBulkImportView.as_view(), name='webemail_import'),
    # path('web-emails/edit/', views.WebEmailBulkEditView.as_view(), name='webemail_bulk_edit'),
    # path('web-emails/delete/', views.WebEmailBulkDeleteView.as_view(), name='webemail_bulk_delete'),
    # path('web-emails/<int:pk>/', include(get_model_urls('wim', 'webemail'))),

    # Software, Tech, Webserver Frameworks
    path('software/', views.SoftwareListView.as_view(), name='software_list'),
    path('software/add/', views.SoftwareEditView.as_view(), name='software_add'),
    path('software/import/', views.SoftwareBulkImportView.as_view(), name='software_import'),
    path('software/edit/', views.SoftwareBulkEditView.as_view(), name='software_bulk_edit'),
    path('software/delete/', views.SoftwareBulkDeleteView.as_view(), name='software_bulk_delete'),
    path('software/<int:pk>/', include(get_model_urls('wim', 'software'))),

    # CPEs
    # path('cpes/', views.CPEListView.as_view(), name='cpe_list'),
    # path('cpes/add/', views.CPEEditView.as_view(), name='cpe_add'),
    # path('cpes/import/', views.CPEBulkImportView.as_view(), name='cpe_import'),
    # path('cpes/edit/', views.CPEBulkEditView.as_view(), name='cpe_bulk_edit'),
    # path('cpes/delete/', views.CPEBulkDeleteView.as_view(), name='cpe_bulk_delete'),
    # path('cpes/<int:pk>/', include(get_model_urls('wim', 'cpe'))),

    # T
    # path('<model_path>/', views.{{model_name}}ListView.as_view(), name='{{model_name}}_list'),
    # path('/add/', views.{{model_name}}EditView.as_view(), name='{{model_name}}_add'),
    # path('/import/', views.{{model_name}}BulkImportView.as_view(), name='{{model_name}}_import'),
    # path('/edit/', views.{{model_name}}BulkEditView.as_view(), name='{{model_name}}_bulk_edit'),
    # path('/delete/', views.{{model_name}}BulkDeleteView.as_view(), name='{{model_name}}_bulk_delete'),
    # path('/<int:pk>/', include(get_model_urls('wim', ''))),
]
