from django.db.models import Q


WEBSITE_IMAGE_FORMATS = 'image/bmp,image/gif,image/jpeg,image/png,image/tiff,image/webp'

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
        'height': 3,
        'color': 'orange',
        'title': 'WEB INVENTORY (WIM)',
        'config': {
            'models': [
                'wim.domain',
                'wim.fqdn',
                'wim.software',
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
