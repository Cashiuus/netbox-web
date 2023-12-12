
from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS
from django.utils import timezone

from netbox.config import Config
from wim.models import Certificate


class Command(BaseCommand):
    help = "Perform housekeeping on TLS certificates records to remove orphaned records no longer tied to any resources."

    def handle(self, *args, **options):
        config = Config()
        cutoff = timezone.now()
        # If this works, refactor to store the query itself, then call `if stale_records.count()` and
        # re-use the variable as the QuerySet object
        # - Help Docs: https://docs.djangoproject.com/en/5.0/topics/db/queries/
        stale_records = Certificate.objects.filter(fqdn__isnull=True, date_expiration__lt=cutoff)
        if stale_records.count():
            if options['verbosity']:
                self.stdout.write(
                    f"Deleting {stale_records.count():,d} stale Certificate records... ",
                    self.style.WARNING,
                    ending=""
                )
                self.stdout.flush()

            # Execute the deletion
            # Certificate.objects.filter(fqdn__isnull=True, date_expiration__lt=cutoff)._raw_delete(using=DEFAULT_DB_ALIAS)
            stale_records._raw_delete(using=DEFAULT_DB_ALIAS)

            if options['verbosity']:
                self.stdout.write("Done.", self.style.SUCCESS)
                self.stdout.write("Deleted Certificates:")
                for object in stale_records:
                    self.stdout.write(f"\n - Cert hash: {object.hash_sha1} - {object.scn}")

        elif options["verbosity"]:
            self.stdout.write("No stale certificate records found.", self.style.SUCCESS)
