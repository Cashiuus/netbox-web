from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from utilities.choices import ChoiceSet



# ========== netbox way of doing choices ============

#
# Primary Status Choices
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
        (STATUS_DECOMMISSIONING, 'Decommissioning', 'red'),
        (STATUS_RETIRED, 'Retired', 'gray'),
    ]


class FQDNOpsStatusChoices(ChoiceSet):
    FQDNSTATUS_1 = "1-whois"
    FQDNSTATUS_2 = "2-dns"
    FQDNSTATUS_3A = "3-parked"
    FQDNSTATUS_3B = "3-redirect"
    FQDNSTATUS_4 = "4-serverdown"
    FQDNSTATUS_5 = "5-active"
    
    CHOICES = (
        (FQDNSTATUS_1, "1-WHOIS", "gray"),
        (FQDNSTATUS_2, "2-DNS", "green"),
        (FQDNSTATUS_3A, "3-PARKED", "gray"),
        (FQDNSTATUS_3B, "3-REDIRECT", "cyan"),
        (FQDNSTATUS_4, "4-DNS SERVER DOWN", "orange"),
        (FQDNSTATUS_5, "5-ACTIVE", "blue"),
    )


class WebsiteOpsStatusChoices(ChoiceSet):
    WEBSITESTATUS_GOOD = "live_good"
    WEBSITESTATUS_BROKEN = "live_broken"
    WEBSITESTATUS_DEFAULT = "live_default"
    WEBSITESTATUS_NONPROD = "live_nonprod"
    # WEBSITESTATUS_
    # WEBSITESTATUS_
    # WEBSITESTATUS_

    CHOICES = (
        (WEBSITESTATUS_GOOD, "Live Website Good", "green"),
        (WEBSITESTATUS_BROKEN, "Live Broken Website", "orange"),
        (WEBSITESTATUS_DEFAULT, "Live Default Webserver", "orange"),
        (WEBSITESTATUS_NONPROD, "Live Nonprod Sister Website", "purple"),
    )




#
# Supporting Data Choices
#


class AssetClassChoices(ChoiceSet):
    ASSET_DOMAIN = "domain"
    ASSET_FQDN = "fqdn"

    CHOICES = (
        (ASSET_DOMAIN, 'Domain', 'blue'),
        (ASSET_FQDN, 'FQDN', 'cyan'),
    )


class CloudProviderChoices(ChoiceSet):
    CLOUD_AWS = "aws"
    CLOUD_AZURE = "azure"
    CLOUD_GOOGLE = "google"
    CLOUD_ALIBABA = "alibaba"

    CHOICES = [
        (CLOUD_AWS, "AWS", "orange"),
        (CLOUD_AZURE, "Azure",  "blue"),
        (CLOUD_GOOGLE, "Google", "cyan"),
        (CLOUD_ALIBABA, "Alibaba", "red"),
    ]



class GeoRegionChoices(ChoiceSet):
    REGION_AMER = "AMER"
    REGION_APAC = "APAC"
    REGION_EMEA = "EMEA"
    REGION_GLOBAL = "GLOBAL"

    CHOICES = [
        (REGION_AMER, "AMER", "gray"),
        (REGION_APAC, "APAC", "gray"),
        (REGION_EMEA, "EMEA", "gray"),
        (REGION_GLOBAL, "GLOBAL", "gray"),
    ]


# TODO: How should I best handle N/A type responses for certain web properties?
class HostingArchModelChoices(ChoiceSet):
    HOSTARCH_CLOUD = "cloud"          # This would be "hybrid" in ServiceNow
    HOSTARCH_ONPREM = "onpremise"
    HOSTARCH_SAAS = "saas"

    CHOICES = (
        (HOSTARCH_CLOUD, "Cloud", "orange"),
        (HOSTARCH_ONPREM, "On-Premise", "cyan"),
        (HOSTARCH_SAAS, "SaaS", "purple"),
    )


class HostingEnvModelChoices(ChoiceSet):
    HOSTENV_DEMO = "demo"
    HOSTENV_DEV = "dev"
    HOSTENV_PROD = "prod"
    HOSTENV_QA = "qa"
    HOSTENV_STAGE = "staging"
    HOSTENV_TEST = "test"
    HOSTENV_TRAIN = "training"
    HOSTENV_DR = "dr"

    CHOICES = (
        (HOSTENV_DEMO, "Demo", "gray"),
        (HOSTENV_DEV, "Dev", "orange"),
        (HOSTENV_PROD, "Prod", "blue"),
        (HOSTENV_QA, "QA", "orange"),
        (HOSTENV_STAGE, "Staging", "orange"),
        (HOSTENV_TEST, "Test", "orange"),
        (HOSTENV_TRAIN, "Training", "gray"),
        (HOSTENV_DR, "DR", "blue"),
    )

# SITE_ENV_CHOICES = Choices(
#     (1, 'demonstration', _('Demonstration')),
#     (2, 'development', _('Development')),
#     (3, 'production', _('Production')),
#     (4, 'qa', _('QA')),
#     (5, 'staging', _('Staging')),
#     (6, 'test', _('Test')),
#     (7, 'training', _('Training')),
#     (8, 'dr', _('DR')),                         # BC/DR
#     (9, 'unknown', _('Unknown')),
#     (10, 'na', _('NA'))
# )


class RedirectStatusChoices(ChoiceSet):
    REDIRECT_GOOD = 'good'
    REDIRECT_BAD = 'bad'
    REDIRECT_UNKNOWN = 'unknown'

    CHOICES = (
        (REDIRECT_GOOD, 'Good', 'green'),
        (REDIRECT_BAD, 'Bad', 'red'),
        (REDIRECT_UNKNOWN, 'Unknown', 'yellow'),
    )


class WebAuthChoices(ChoiceSet):
    AUTH_BASIC = "basic_auth"
    AUTH_SSO_CORP = "sso_corp"
    AUTH_SSO_OTHER = "sso_other"
    AUTH_STANDALONE = "standalone"

    CHOICES = [
        (AUTH_BASIC, 'Basic Auth', 'orange'),
        (AUTH_SSO_CORP, 'SSO-Corp', 'blue'),
        (AUTH_SSO_OTHER, 'SSO-Other', 'blue'),
        (AUTH_STANDALONE, 'Standalone', 'orange'),
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

