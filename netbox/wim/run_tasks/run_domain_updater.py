
from wim.models import Domain



def update_domain():
    


def update_all_domains():

    # Here is how you get a flat list of only the domain names
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
