from django.urls import path

from netbox.api.routers import NetBoxRouter
from . import views


app_name = "wim-api"


router = NetBoxRouter()
router.APIRootView = views.WIMRootView

router.register('domains', views.DomainViewSet)
router.register('fqdns', views.FQDNViewSet)


urlpatterns = [
    # TODO: This is actually meant to get "available" things like IP's not used in a range, etc.
    # Unsure how i might use this particular feature...
    # path(
    #     'domains/<int:pk>/'
    # )
]

urlpatterns += router.urls
