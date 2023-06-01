
# If a domain has not been recon scanned since x time, run full enumeration workflow on it.
# Then, update its last recon scanned date.


from datetime import datetime

from wim.models import Domain, FQDN




def get_outdated_records():

    # If last recon date is more than 14 days ago, include it in scope
    threshold_date = datetime.timedelta(datetime.todays_date() - 14)
    domains = Domain.objects.filter(date_last_recon_scanned__lt=threshold_date)
    for d in domains:
        # do recon workflow
        # dataset = enumerate_single_domain(d)
        pass

        # TOOD: See here to implement this: https://www.reddit.com/r/django/comments/mjpbij/running_a_bulk_update_efficiently_with_django/?onetap_auto=true
        
        # How to update the domain's last scanned date:
        # domains.update(date_last_recon_scanned=datetime.now())
    

    return


