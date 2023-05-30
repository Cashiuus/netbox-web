from django.db.models import Q

# from .choices import FHRPGroupProtocolChoices, IPAddressRoleChoices


#
# VRFs
#

# Per RFC 4364 section 4.2, a route distinguisher may be encoded as one of the following:
#   * Type 0 (16-bit AS number : 32-bit integer)
#   * Type 1 (32-bit IPv4 address : 16-bit integer)
#   * Type 2 (32-bit AS number : 16-bit integer)
# 21 characters are sufficient to convey the longest possible string value (255.255.255.255:65535)
# Also used for RouteTargets
VRF_RD_MAX_LENGTH = 21


#
# Prefixes
#

PREFIX_LENGTH_MIN = 1
PREFIX_LENGTH_MAX = 127  # IPv6


#
# IPAddresses
#

IPADDRESS_ASSIGNMENT_MODELS = Q(
    Q(app_label='dcim', model='interface') |
    Q(app_label='ipam', model='fhrpgroup') |
    Q(app_label='virtualization', model='vminterface')
)

IPADDRESS_MASK_LENGTH_MIN = 1
IPADDRESS_MASK_LENGTH_MAX = 128  # IPv6

# IPADDRESS_ROLES_NONUNIQUE = (
#     # IPAddress roles which are exempt from unique address enforcement
#     IPAddressRoleChoices.ROLE_ANYCAST,
#     IPAddressRoleChoices.ROLE_VIP,
#     IPAddressRoleChoices.ROLE_VRRP,
#     IPAddressRoleChoices.ROLE_HSRP,
#     IPAddressRoleChoices.ROLE_GLBP,
#     IPAddressRoleChoices.ROLE_CARP,
# )




#
# Services
#

# 16-bit port number
SERVICE_PORT_MIN = 1
SERVICE_PORT_MAX = 65535

L2VPN_ASSIGNMENT_MODELS = Q(
    Q(app_label='dcim', model='interface') |
    Q(app_label='ipam', model='vlan') |
    Q(app_label='virtualization', model='vminterface')
)
