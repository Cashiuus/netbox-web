from django.utils.text import slugify

from extras.scripts import Script, ObjectVar, StringVar
from utilities.exceptions import AbortScript
from wim.models import Domain, FQDN
from wim.choices import (
    DomainStatusChoices, DomainOwnershipStatusChoices, 
    FQDNStatusChoices, FQDNOpsStatusChoices,
)


# Help: https://docs.netbox.dev/en/stable/customization/custom-scripts/


# All custom scripts must inherit this Script base class so that
# forms and logging are functional
class DomainScanScript(Script):
    # Scripts compromise of at least 2 components: variables (for user input), and a run() method
    domain_new = StringVar(
        label=_('New Domain'),
        required=False,
    )

    domain = ObjectVar(
        model=Domain,
        required=False,
        query_params={'date_last_recon_scanned': None},     # Return all records w/o a date
        null_option=True,      # Use this so if user chooses blank, run scan on all returned domains in bulk
    )

    # name can be defined, but will be the python filename if not specified
    # name = ""

    class Meta:
        # -- Attributes go here, all optional --

        name = "Run Domain Scan"
        description = "Run a fresh domain scan on a new or existing domain"

        # By default, fields will be ordered in same order they are defined in this class
        field_order = ('domain_new', 'domain')

        # If this is defined, field_order will be ignored
        # At the very end, a "Script Execution Parameters" group will be added by default for the user
        # fieldsets = ()

        # NOTE: We can only schedule a script like this if it auto-scans things rather than requires user input
        # commit_default = True
        # scheduling_enabled = True
        # If not used, RQ_DEFAULT_TIMEOUT will be used for this default value
        # job_timeout = 



    def run(self, data, commit=True):
        # run method should accept 2 args, data:dict, and commit:bool
        pass

        # Accessing request data: https://docs.djangoproject.com/en/stable/ref/request-response/
        username = self.request.user.username
        domain = None
        if data.get('domain_new'):
            self.log_info("New domain selected for scan")
            domain = Domain(
                name=data.get('domain_new'),
                slug=slugify(data['domain_new']),
                status=DomainStatusChoices.STATUS_NEW,
            )
        elif data.get('domain'):
            self.log_info("Existing domain chosen from list for scan")
            domain = Domain(
                name=data.get('domain'),
                status=DomainStatusChoices.STATUS_ACTIVE,
            )
        
        # results = run_domain_updater(domain)


        # If you wish to make changes to an object, you must snapshot first for change logging to work
        # before changing data
        if domain.pk and hasattr(domain, 'snapshot'):
            domain.snapshot()
        
        # Now, data can be changed
        # obj.property = "new value"
        # obj.full_clean()
        # obj.save()


        # Error handling
        # if some_error:
        #     raise AbortScript("Error during script execution with etc...")

        if domain:
            domain.full_clean()
            domain.save()
            self.log_success(f"Finished scanning {domain}")
        return






# If you need to change the default order of scripts shown in list view, do it this way:
# script_order = (Script1, Script2, etc...)
