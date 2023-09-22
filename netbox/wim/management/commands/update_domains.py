from django.core.management.base import BaseCommand

# from ipam.models import Prefix, VRF
# from ipam.utils import rebuild_prefixes
from wim.models import Domain
from wim.run_tasks.run_domain_updater import update_domains


class Command(BaseCommand):
    help = "Update Whois registration data for domains"

    def handle(self, *model_names, **options):
        self.stdout.write(f"Updating {Domain.objects.count()} domains...")

        # Do the tasks
        # domains_list = list(Domain.objects.values_list('name', flat=True))
        # update_domains(domains_list)
        update_domains()


        self.stdout.write(self.style.SUCCESS("Update complete"))
        return
