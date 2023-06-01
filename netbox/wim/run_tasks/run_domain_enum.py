
# If a domain has not been recon scanned since x time, run full enumeration workflow on it.
# Then, update its last recon scanned date.


from datetime import datetime

from wim.models import Domain, FQDN




def get_outdated_records():

    # If last recon date is more than 14 days ago, include it in scope
    threshold = datetime.timedelta(datetime.todays_date() - 14)
    domains = Domain.objects.filter(date_last_recon_scanned__lt=threshold)
    for d in domains:
        # do recon workflow
        # dataset = enumerate_single_domain(d)
        pass
    

    return


