from django.db.models import Manager

# from ipam.lookups import Host, Inet
from utilities.querysets import RestrictedQuerySet

class FQDNManager(Manager.from_queryset(RestrictedQuerySet)):
    pass
    # def get_queryset(self):
    #     """
        
    #     """