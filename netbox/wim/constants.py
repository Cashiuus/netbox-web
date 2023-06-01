from django.db.models import Q

# from .choices import FHRPGroupProtocolChoices, IPAddressRoleChoices


#
# WIM Dashboard Widgets
#
# TODO: The default dashboard is stored in extras/constants.py
# How can I efficiently stand up this widget as part of the standard for all users
# Don't want them to have to create a custom one, unless I can create it and it's shared.
WIM_DASHBOARD = [
    {
        'widget': 'extras.ObjectCountsWidget',
        'width': 4,
        'height': 2,
        'color': 'orange',
        'title': 'WEB INVENTORY (WIM)',
        'config': {
            'models': [
                'wim.domain',
                'wim.fqdn',
            ]
        }
    },
]



#
# Services
#

# 16-bit port number
SERVICE_PORT_MIN = 1
SERVICE_PORT_MAX = 65535
