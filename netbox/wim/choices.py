from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from utilities.choices import ChoiceSet



# ========== netbox way of doing choices ============

#
# Domains
#

class DomainStatusChoices(ChoiceSet):
    key = 'Domain.status'

    STATUS_NEW = 'new'
    STATUS_ACTIVE = 'active'
    STATUS_DECOMMISSIONING = 'decommissioning'
    STATUS_RETIRED = 'retired'

    CHOICES = [
        # (STATUS_PLANNED, 'Planned', 'cyan'),
        (STATUS_NEW, 'New', 'blue'),
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_DECOMMISSIONING, 'Decommissioning', 'yellow'),
        (STATUS_RETIRED, 'Retired', 'red'),
    ]


#
# FQDNs
#

class FQDNStatusChoices(ChoiceSet):
    key = 'FQDN.status'

    STATUS_NEW = 'new'
    STATUS_ACTIVE = 'active'
    STATUS_DECOMMISSIONING = 'decommissioning'
    STATUS_RETIRED = 'retired'

    CHOICES = [
        # (STATUS_PLANNED, 'Planned', 'cyan'),
        (STATUS_NEW, 'New', 'blue'),
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_DECOMMISSIONING, 'Decommissioning', 'yellow'),
        (STATUS_RETIRED, 'Retired', 'red'),
    ]


class WebAuthChoices(ChoiceSet):
    AUTH_BASIC = "basic_auth"
    AUTH_SSO_CORP = "sso_corp"
    AUTH_SSO_OTHER = "sso_other"
    AUTH_STANDALONE = "standalone"

    CHOICES = [
        (AUTH_BASIC, 'Basic Auth', 'cyan'),
        (AUTH_SSO_CORP, 'SSO-Corp', 'cyan'),
        (AUTH_SSO_OTHER, 'SSO-Other', 'cyan'),
        (AUTH_STANDALONE, 'Standalone', 'cyan'),
    ]


class WebsiteRoleChoices(ChoiceSet):
    ROLE_ECOMMERCE = 'ecommerce'
    ROLE_INFORMATIONAL = 'informational'
    ROLE_INTERNAL = 'internal'
    ROLE_MARKETING = 'marketing'
    ROLE_OTHER = 'other'

    CHOICES = (
        (ROLE_ECOMMERCE, 'E-Commerce', 'green'),
        (ROLE_INFORMATIONAL, 'Informational', 'blue'),
        (ROLE_INTERNAL, 'Internal', 'orange'),
        (ROLE_MARKETING, 'Marketing', 'purple'),
        (ROLE_OTHER, 'Other', 'yellow'),
    )


class AssetClassChoices(ChoiceSet):
    ASSET_DOMAIN = "domain"
    ASSET_FQDN = "fqdn"

    CHOICES = (
        (ASSET_DOMAIN, 'Domain', 'blue'),
        (ASSET_FQDN, 'FQDN', 'cyan'),
    )


class RedirectStatusChoices(ChoiceSet):
    REDIRECT_GOOD = 'good'
    REDIRECT_BAD = 'bad'
    REDIRECT_UNKNOWN = 'unknown'

    CHOICES = (
        (REDIRECT_GOOD, 'Good', 'green'),
        (REDIRECT_BAD, 'Bad', 'red'),
        (REDIRECT_UNKNOWN, 'Unknown', 'yellow'),
    )


# ========== my original way of doing choices ============

RECORD_STATUS_CHOICES = Choices(
    (1, 'active', _('Active')),             # active records in our inventory
    (2, 'archive', _('Archive')),           # records we've divested, stopped owning, etc, but "used to own"
    (3, 'delete', _('Delete')),             # marked for deletion because we never owned them, invalid entries
    (4, 'new', _('New')),                   # new entries requiring validation and moved to "active/confirmed" status
)

INV_STATUS_CHOICES = Choices(
    (1, 'candidate', _('Candidate')),               # Ingested via scan data and needs verified
    (2, 'confirmed', _('Confirmed')),               # valid/vetted inventory
    (3, 'rejected', _('Rejected')),                 # rejected after vetting as not ours
)

# Nevermind, probably setup different tables for different asset types in the future version of this.
ASSET_TYPE_CHOICES = Choices(
    (1, 'asn', _('ASN')),
    (2, 'fqdn', _('FQDN')),
    (3, 'ip_subnet', _('IP_Subnet')),
)

GEO_REGION_CHOICES = Choices(
    (1, 'amer', _('AMER')),
    (2, 'apac', _('APAC')),
    (3, 'emea', _('EMEA')),
    (4, 'global', _('Global')),
)

COMPLIANCE_CHOICES = Choices(
    (1, 'cdi', _('CDI')),
    (2, 'gtc', _('gtc')),
    (3, 'gxp', _('GxP')),
    (4, 'hipaa', _('HIPAA')),
    (5, 'kisms', _('K-ISMS')),
    (6, 'pci', _('PCI')),
    (7, 'sox', _('SOX'))
)

CMDB_ARCH_MODEL = Choices(
    (1, 'hybrid', _('Hybrid')),             # hybrid = cloud for our purposes
    (2, 'onpremise', _('On-Premise')),      # hosted on premise
    (3, 'saas', _('SaaS')),                 # SaaS = vendor/3rd party hosted for our purposes
    (4, 'na', _('NA')),                     # N/A - not an asset that is "hosted"
)

HOSTING_ARCH_MODEL = Choices(
    (1, 'cloud', _('Cloud')),
    (2, 'onpremise', _('On-Premise')),
    (3, 'saas', _('SaaS')),
    (4, 'unknown', _('Unknown')),
    (5, 'na', _('NA')),
)

FQDN_STATUS_CHOICES = Choices(
    (1, 'active', _('active')),                 # FQDN with IP: and valid content serving website
    (2, 'parked', _('Parked')),                 # FQDN with IP: parked website in good health
    (3, 'redirect', _('Redirect')),             # FQDN with IP: perm redirect website in good health
    (4, 'defensive', _('defensive')),           # FQDN with no IP, this is only a WHOIS registered domain
    (5, 'reseller', _('Reseller')),             # Not owned by us, but is an authorized distributor/reseller
    (6, 'invalid', _('Invalid')),               # An invalid FQDN that we don't actually own, or we let go of
)

REDIRECT_STATUS_CHOICES = Choices(
    (1, 'na', _('N/A')),                        # Meaning: this entry is not supposed to have a redirect
    (2, 'good', _('Good')),                     # 301 permanent redirect in good shape, no errors
    (3, 'temporary', _('Temporary')),           # 302 or temporary redirect
    (4, 'broken', _('Broken')),                 # Mis-configured or inadequate redirect in place
    (5, 'unknown', _('Unknown/Test')),               # Meaning: hasn't yet been tested and needs follow-up
    (6, 'housekeeping', _('Needs Housekeeping')),   # Poor or inefficient redirect that needs tuning/housekeeping
)

SITE_ENV_CHOICES = Choices(
    (1, 'demonstration', _('Demonstration')),
    (2, 'development', _('Development')),
    (3, 'production', _('Production')),
    (4, 'qa', _('QA')),
    (5, 'staging', _('Staging')),
    (6, 'test', _('Test')),
    (7, 'training', _('Training')),
    (8, 'dr', _('DR')),                         # BC/DR
    (9, 'unknown', _('Unknown')),
    (10, 'na', _('NA'))
)

OS_ARCH_CHOICES = Choices(
    (1, 'x86', _('x86')),
    (2, 'x64', _('x64'))
)

LAYER_SECURITY_CHOICES = Choices(
    (1, 'tls13', _('TLS 1.3')),
    (1, 'tls12', _('TLS 1.2')),
    (1, 'tls11', _('TLS 1.1')),
    (1, 'tls10', _('TLS 1.0')),
    (1, 'ssl30', _('SSL 3.0')),
)

CONFIDENCE_CHOICES = Choices(
    (1, 'candidate', _('Candidate')),
    (2, 'confirmed', _('Confirmed')),
    (3, 'dismissed', _('Dismissed'))
)

IMPORTANCE_CHOICES = Choices(
    (1, 'critical', _('Critical')),
    (2, 'high', _('High')),
    (3, 'medium', _('Medium')),
    (4, 'low', _('Low')),
    (5, 'unknown', _('Unknown')),
)

SUPPORT_GROUP_TYPE_CHOICES = Choices(
    (1, 'servicenow', _('ServiceNow Group')),
    (2, 'teamname', _('Team/Dept Name')),
)

