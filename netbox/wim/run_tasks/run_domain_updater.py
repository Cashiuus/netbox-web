from django.utils.text import slugify

from extras.scripts import Script, ChoiceVar, StringVar
from utilities.exceptions import AbortScript
from wim.models import Domain, FQDN
from wim.choices import DomainOwnershipStatusChoices


class NewDomainScript(Script):
    """
    A custom workflow for adding a new Domain Root by retrieving all technical data.
    """
    class Meta:
        name = "New Domain"
        description = "Fetch technical data and add new domain to inventory"

    domain_name = StringVar(description="New root domain to be added")

    ownership_type = ChoiceVar(
        DomainOwnershipStatusChoices,
        description="Ownership Type",
        required=False,
    )

    def run(self, data, commit):
        """ Mandatory method to run this script. """
        # Take the submitted domain, check it's not already in db?




class DomainWhoisUpdaterSingle(Script):
    """
    Update a single domain record's Whois registration data.
    """

    class Meta:
        name = "Domain Whois Updater Script - Single"
        description = "Run a scan on the domain for updated Whois data and save to the database."
        # commit_default = True
        # scheduling_enabled = True
        job_timeout = 300


    def run(self, data, commit):
        """ Required method that runs the execution of this script class. """
        pass





class DomainWhoisUpdaterFull(Script):
    """
    Update all active domain records' Whois registration data.

    Custom Scripts Docs: https://docs.netbox.dev/en/stable/customization/custom-scripts/
    """

    class Meta:
        name = "Domain Whois Updater Script - Bulk"
        description = "Run a scan on the domain for updated Whois data and save to the database."
        # commit_default = True
        # scheduling_enabled = True
        job_timeout = 6000


    def run(self, data, commit):
        """ Required method that runs the execution of this script class. """

        # Here is how you get a flat list of only the domain names
        # TODO: Change query and only get domains that are active
        domains_queryset = Domain.objects.all()
        domains_list = list(Domain.objects.values_list('name', flat=True))
        # Run my updater stuff, counting how many records we've done along the way

        counter = 0
        update_queue = []
        for d in domains_list:
            # Handle saving updates in bulk, everytime we have 100 updates, do them

            # Run whois collection and add saved data to queue list

            update_queue.append(
                # TODO: How to add the record's data like this?
                Domain()
            )

            if len(update_queue) >= 100:
                # Bulk update and reset the queue
                # TODO: How to update DB properly this way?
                Domain.objects.bulk_update(update_queue, [], batch_size=100)
                update_queue = []

        # Finally, if queue still has data (e.g. under 100) after loop ends, update
        Domain.objects.bulk_update(update_queue, [])
        # and we're done
        return
