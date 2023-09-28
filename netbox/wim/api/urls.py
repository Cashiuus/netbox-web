# from django.urls import path

from netbox.api.routers import NetBoxRouter
from . import views


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
router.register('software', views.SoftwareViewSet)


app_name = "wim-api"
urlpatterns = router.urls
