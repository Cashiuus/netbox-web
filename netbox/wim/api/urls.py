# from django.urls import path

from netbox.api.routers import NetBoxRouter
from . import views


app_name = "wim-api"

router = NetBoxRouter()
router.APIRootView = views.WIMRootView

router.register('domains', views.DomainViewSet)
router.register('fqdns', views.FQDNViewSet)
router.register('brands', views.BrandViewSet)
router.register('business-groups', views.BusinessGroupViewSet)
router.register('business-divisions', views.BusinessDivisionViewSet)
# router.register('business-criticalities', views.BusinessCriticalityViewSet)
router.register('operating-systems', views.OperatingSystemViewSet)
router.register('site-locations', views.SiteLocationViewSet)
router.register('vendors', views.VendorViewSet)
router.register('webemails', views.WebEmailViewSet)
router.register('webserver-frameworks', views.WebserverFrameworkViewSet)



# urlpatterns = [
#     # TODO: This is actually meant to get "available" things like IP's not used in a range, etc.
#     # Unsure how i might use this particular feature...
#     # path(
#     #     'domains/<int:pk>/'
#     # )
# ]

# urlpatterns += router.urls
urlpatterns = router.urls
