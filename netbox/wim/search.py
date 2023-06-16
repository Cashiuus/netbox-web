# File Purpose: This enables searches from the top-center global search box
#               More specifically, this sets up indices on the defined fields
#               You'll define a fieldname and a weight value (int)
#               I *think* lower weight value means more important
#
#   Note: This file alone, doesn't enable global search, something else is also needed.


from netbox.search import SearchIndex, register_search
from . import models


@register_search
class FQDNIndex(SearchIndex):
    model = models.FQDN
    # (fieldname, weight)
    fields = (
        ('name', 100),
        ('public_ip_1', 200),
        ('owners_orig', 500),
    )
    

@register_search
class DomainIndex(SearchIndex):
    model = models.Domain
    fields = (
        ('name', 100),
    )
