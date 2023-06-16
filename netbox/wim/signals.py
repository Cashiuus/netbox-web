# File Purpose: This file is for handling signals in order to help keep the DB clean
#               based on its intended design.


from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver

# from dcim.models import Device
# from virtualization.models import VirtualMachine
# from ipam.models import IPAddress, Prefix
from .models import Domain, FQDN


# TODO: Any signals for post- actions?



# Use Case: If an asset was previously active and is now unused, update all affected data
@receiver(post_save, sender=FQDN)
def update_decommissioned_fqdns(instance, created, **kwargs):
    """
    Update records that, based on recon updates, are no longer active assets.
    """
    # They are not new records, already existed
    # TODO: Unsure how to implement this
    if not created:
        # old_fqdn_status = FQDN()
        pass

