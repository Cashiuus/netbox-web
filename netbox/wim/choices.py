from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from utilities.choices import ChoiceSet



# ========== netbox way of doing choices ============


# NOTE: from the utilities/choices.py file, these are the possible button color choices:
# DEFAULT = 'outline-dark'
# BLUE = 'blue'
# INDIGO = 'indigo'
# PURPLE = 'purple'
# PINK = 'pink'
# RED = 'red'
# ORANGE = 'orange'
# YELLOW = 'yellow'
# GREEN = 'green'
# TEAL = 'teal'
# CYAN = 'cyan'
# GRAY = 'gray'
# GREY = 'gray'  # Backward compatability for <3.2
# BLACK = 'black'
# WHITE = 'white'



#
# Primary Status Choices
#


class AssetConfidenceChoices(ChoiceSet):
    # Choose the level of confidence in attribution for a particular discovered asset (Domain, FQDN, etc)
    # Candidate = found during recon and requires manual validation or vetting
    # Confirmed = Confirmed to belong to attributed entity
    # Dismissed = Determined the asset is not in fact owned by the entity for which it was a candidate
    # TODO: WTF is this key used for
    key = 'FQDN.asset_confidence'

    CONFIDENCE_CANDIDATE = "Candidate"
    CONFIDENCE_CONFIRMED = "Confirmed"
    CONFIDENCE_DISMISSED = "Dismissed"

    # NOTE: CHOICES must be a list type (not tuple) if you have a "key" var defined
    CHOICES = [
        (CONFIDENCE_CANDIDATE, "Candidate", "orange"),
        (CONFIDENCE_CONFIRMED, "Confirmed", "green"),
        (CONFIDENCE_DISMISSED, "Dismissed", "gray"),
    ]


class AssetStatusReasonChoices(ChoiceSet):
    """ The reasons behind why an asset has a particular status.
    """
    REASON_PERSONAL = "Personal Registration"
    REASON_DECOMISSIONED = "Decommissioned Website"
    REASON_DIVESTED = "Divested"

    CHOICES = [
        (REASON_PERSONAL, "Personal Registration", "gray"),
        (REASON_DECOMISSIONED, "Decommissioned Website", "gray"),
        (REASON_DIVESTED, "Divested", "gray"),
    ]


class DomainStatusChoices(ChoiceSet):
    key = 'Domain.status'

    STATUS_NEW = 'New'
    STATUS_ACTIVE = 'Active'
    STATUS_DECOMMISSIONING = 'Decommissioning'
    STATUS_RETIRED = 'Archived'

    CHOICES = [
        # (STATUS_PLANNED, 'Planned', 'cyan'),
        (STATUS_NEW, 'New', 'orange'),
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_DECOMMISSIONING, 'Decommissioning', 'purple'),
        (STATUS_RETIRED, 'Archived', 'gray'),
    ]


class FQDNStatusChoices(ChoiceSet):
    key = 'FQDN.status'

    STATUS_NEW = 'New'
    STATUS_ACTIVE = 'Active'
    STATUS_DECOMMISSIONING = 'Decommissioning'
    STATUS_RETIRED = 'Archived'

    CHOICES = [
        # (STATUS_PLANNED, 'Planned', 'cyan'),
        (STATUS_NEW, 'New', 'orange'),
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_DECOMMISSIONING, 'Decommissioning', 'purple'),
        (STATUS_RETIRED, 'Archived', 'gray'),
    ]


class FQDNOpsStatusChoices(ChoiceSet):
    FQDNSTATUS_UNKNOWN = "0-Unknown-Test"
    FQDNSTATUS_1 = "1-Whois"
    FQDNSTATUS_2 = "2-DNS"
    FQDNSTATUS_4 = "2-DNS Host Server Down"
    FQDNSTATUS_3A = "3-Parked"
    FQDNSTATUS_3B = "3-Redirect"
    FQDNSTATUS_5 = "5-Active"
    FQDNSTATUS_NA = "NA"

    CHOICES = (
        (FQDNSTATUS_UNKNOWN, "0-Unknown-Test", "orange"),
        (FQDNSTATUS_1, "1-Whois", "gray"),
        (FQDNSTATUS_2, "2-DNS", "cyan"),
        (FQDNSTATUS_4, "2-DNS Host Server Down", "cyan"),
        (FQDNSTATUS_3A, "3-Parked", "pink"),
        (FQDNSTATUS_3B, "3-Redirect", "pink"),
        (FQDNSTATUS_5, "5-Active", "green"),
        (FQDNSTATUS_NA, "NA", "gray"),
    )


class WebsiteOpsStatusChoices(ChoiceSet):
    WEBSITESTATUS_UNKNOWN = "0-Unknown-Test"
    WEBSITESTATUS_NONSITE = "3-Live Non-Website Server"
    WEBSITESTATUS_DEFAULT = "4-Live Default Webserver"
    WEBSITESTATUS_BROKEN = "4-Live Broken Website"
    WEBSITESTATUS_CUSTOMSPLASH = "4-Live Custom Parked Website"     # A site with a custom splash/parked page still served from a server
    WEBSITESTATUS_GOOD = "5-Live Valid Website"
    # WEBSITESTATUS_NONPROD = "6-Live Nonprod Sister Website"
    WEBSITESTATUS_DUPEDOMAIN = "6-Live Domain WWW Pointer"      # A domain website duplicate of its www FQDN
    WEBSITESTATUS_DECOMMISSIONED = "9-Decommissioned"
    WEBSITESTATUS_NA = "NA"

    CHOICES = (
        (WEBSITESTATUS_UNKNOWN, "0-Unknown-Test", "red"),
        (WEBSITESTATUS_NONSITE, "3-Live Non-Website Server", "cyan"),
        (WEBSITESTATUS_DEFAULT, "4-Live Default Webserver", "orange"),
        (WEBSITESTATUS_BROKEN, "4-Live Broken Website", "orange"),
        (WEBSITESTATUS_CUSTOMSPLASH, "4-Live Custom Parked Website", "orange"),
        (WEBSITESTATUS_GOOD, "5-Live Valid Website", "green"),
        (WEBSITESTATUS_DUPEDOMAIN, "6-Live Domain WWW Pointer", "gray"),
        # (WEBSITESTATUS_NONPROD, "6-Live Nonprod Sister Website", "gray"),
        (WEBSITESTATUS_DECOMMISSIONED, "9-Decommissioned", "purple"),
        (WEBSITESTATUS_NA, "NA", "gray"),
    )



class DomainOwnershipStatusChoices(ChoiceSet):
    """
    Choices that define categories for root domains in our dataset. Not all are owned by
    this company; many may be related to vendor SaaS offerings, etc.
    """
    OWNEDSTATUS_COMPANY = "Company-Owned"
    OWNEDSTATUS_PROVIDER = "Provider-Owned"
    OWNEDSTATUS_UNKNOWN = "Unknown"

    CHOICES = (
        (OWNEDSTATUS_COMPANY, "Company-Owned", "green"),
        (OWNEDSTATUS_PROVIDER, "Provider-Owned", "purple"),
        (OWNEDSTATUS_UNKNOWN, "Unknown", "red"),
    )



#
# Supporting Data Choices
#

class AssetClassChoices(ChoiceSet):
    ASSET_DOMAIN = "Domain"
    ASSET_FQDN = "FQDN"

    CHOICES = (
        (ASSET_DOMAIN, 'Domain', 'teal'),
        (ASSET_FQDN, 'FQDN', 'cyan'),
    )


class CloudProviderChoices(ChoiceSet):
    CLOUD_AWS = "AWS"
    CLOUD_AZURE = "Azure"
    CLOUD_ALIBABA = "Alibaba"
    CLOUD_DIGOCEAN = "Digital Ocean"
    CLOUD_GOOGLE = "Google"
    CLOUD_ORACLE = "Oracle"

    CHOICES = [
        (CLOUD_AWS, "AWS", "orange"),
        (CLOUD_AZURE, "Azure",  "blue"),
        (CLOUD_ALIBABA, "Alibaba", "gray"),
        (CLOUD_DIGOCEAN, "Digital Ocean", "teal"),
        (CLOUD_GOOGLE, "Google", "cyan"),
        (CLOUD_ORACLE, "Oracle", "red"),
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
    HOSTARCH_CLOUD = "Hybrid"          # This means company-managed cloud
    HOSTARCH_ONPREM = "On-Premise"
    HOSTARCH_SAAS = "SaaS"
    HOSTARCH_NA = "NA"

    CHOICES = (
        (HOSTARCH_CLOUD, "Hybrid", "green"),
        (HOSTARCH_ONPREM, "On-Premise", "cyan"),
        (HOSTARCH_SAAS, "SaaS", "purple"),
        (HOSTARCH_NA, "NA", "gray"),
    )


class HostingEnvModelChoices(ChoiceSet):
    HOSTENV_DEMO = "Demonstration"
    HOSTENV_DEV = "Development"
    HOSTENV_PROD = "Production"
    HOSTENV_QA = "QA"
    HOSTENV_STAGE = "Staging"
    HOSTENV_TEST = "Test"
    HOSTENV_TRAIN = "Training"
    HOSTENV_DR = "BC-DR"
    HOSTENV_NA = "NA"

    CHOICES = (
        (HOSTENV_DEMO, "Demonstration", "gray"),
        (HOSTENV_DEV, "Development", "orange"),
        (HOSTENV_PROD, "Production", "blue"),
        (HOSTENV_QA, "QA", "orange"),
        (HOSTENV_STAGE, "Staging", "orange"),
        (HOSTENV_TEST, "Test", "orange"),
        (HOSTENV_TRAIN, "Training", "orange"),
        (HOSTENV_DR, "BC-DR", "blue"),
        (HOSTENV_NA, "NA", "gray"),
    )


class RedirectStatusChoices(ChoiceSet):
    REDIRECT_GOOD = 'Good'
    REDIRECT_BAD = 'Bad'
    REDIRECT_UNKNOWN = 'Unknown'

    CHOICES = (
        (REDIRECT_GOOD, 'Good', 'green'),
        (REDIRECT_BAD, 'Bad', 'red'),
        (REDIRECT_UNKNOWN, 'Unknown', 'yellow'),
    )


class WebAuthChoices(ChoiceSet):
    AUTH_BASIC = "Basic Auth"
    AUTH_SSO_CORP = "SSO-Corp"
    AUTH_SSO_OTHER = "SSO-Other"
    AUTH_STANDALONE = "Standalone"

    CHOICES = [
        (AUTH_BASIC, 'Basic Auth', 'orange'),
        (AUTH_SSO_CORP, 'SSO-Corp', 'blue'),
        (AUTH_SSO_OTHER, 'SSO-Other', 'blue'),
        (AUTH_STANDALONE, 'Standalone', 'orange'),
    ]


class WebsiteRoleChoices(ChoiceSet):
    ROLE_B2B = "B2B"
    ROLE_CUSTSERVICE = "Customer Service"
    ROLE_ECOMMERCE = 'E-Commerce'
    ROLE_INFORMATIONAL = 'Informational'
    ROLE_INTERNAL = 'Internal'
    ROLE_MARKETING = 'Marketing'
    ROLE_PRODSERVICES = 'Product Services'
    ROLE_OTHER = 'Other'

    CHOICES = (
        (ROLE_B2B, 'B2B', 'green'),
        (ROLE_CUSTSERVICE, 'Customer Service', 'purple'),
        (ROLE_ECOMMERCE, 'E-Commerce', 'green'),
        (ROLE_INFORMATIONAL, 'Informational', 'blue'),
        (ROLE_INTERNAL, 'Internal', 'orange'),
        (ROLE_MARKETING, 'Marketing', 'purple'),
        (ROLE_PRODSERVICES, 'Product Services', 'purple'),
        (ROLE_OTHER, 'Other', 'yellow'),
    )


class TransportLayerSecurityVersionChoices(ChoiceSet):
    TLS_10 = "TLS 1.0"
    TLS_11 = "TLS 1.1"
    TLS_12 = "TLS 1.2"
    TLS_13 = "TLS 1.3"
    TLS_SSL3 = "SSL 3.0"
    TLS_SSL2 = "SSL 2.0"

    CHOICES = (
        (TLS_10, "TLS 1.0", "orange"),
        (TLS_11, "TLS 1.1", "orange"),
        (TLS_12, "TLS 1.2", "green"),
        (TLS_13, "TLS 1.3", "green"),
        (TLS_SSL3, "SSL 3.0", "red"),
        (TLS_SSL2, "SSL 2.0", "red"),
    )



class ComplianceProgramChoices(ChoiceSet):
    COMPLIANCE_CDI = "CDI"
    COMPLIANCE_GTC = "GTC"
    COMPLIANCE_GXP = "GxP"
    COMPLIANCE_HIPAA = "HIPAA"
    COMPLIANCE_HITRUST = "HITRUST"
    COMPLIANCE_KISMS = "K-ISMS"
    COMPLIANCE_PCI = "PCI-DSS"
    COMPLIANCE_SOX = "SOX"

    CHOICES = (
        (COMPLIANCE_CDI, "CDI", "gray"),
        (COMPLIANCE_GTC, "GTC", "gray"),
        (COMPLIANCE_GXP, "GxP", "gray"),
        (COMPLIANCE_HIPAA, "HIPAA", "gray"),
        (COMPLIANCE_HITRUST, "HITRUST", "gray"),
        (COMPLIANCE_KISMS, "K-ISMS", "gray"),
        (COMPLIANCE_PCI, "PCI-DSS", "gray"),
        (COMPLIANCE_SOX, "SOX", "gray"),
    )


class PlatformFamilyChoices(ChoiceSet):
    PLATFORMFAMILY_LINUX = "Linux"
    PLATFORMFAMILY_WINDOWS = "Windows"
    PLATFORMFAMILY_OSX = "OSX"
    PLATFORMFAMILY_OTHER = "Other"

    CHOICES = [
        (PLATFORMFAMILY_LINUX, "Linux", ""),
        (PLATFORMFAMILY_WINDOWS, "Windows", ""),
        (PLATFORMFAMILY_OSX, "OSX", ""),
        (PLATFORMFAMILY_OTHER, "Other", ""),
    ]


class PlatformTypeChoices(ChoiceSet):
    PLATFORMTYPE_SERVER = "Server"
    PLATFORMTYPE_WORKSTATION = "Workstation"
    PLATFORMTYPE_NETWORK = "Network"
    PLATFORMTYPE_OT = "OT"
    PLATFORMTYPE_PERIPHERAL = "Peripheral"      # e.g. Printer, Phone, etc.

    CHOICES = [
        (PLATFORMTYPE_SERVER, "Server", "blue"),
        (PLATFORMTYPE_WORKSTATION, "Workstation", "blue"),
        (PLATFORMTYPE_NETWORK, "Network", "green"),
        (PLATFORMTYPE_OT, "OT", "purple"),
        (PLATFORMTYPE_PERIPHERAL, "Peripheral", "cyan"),
    ]


# TLS Certificate Key Types and Strengths
# ---------------------------------------------------------
class CertSigningAlgorithmChoices(ChoiceSet):
    HASH_SHA1 = "SHA1"
    HASH_SHA160 = "SHA160"
    HASH_SHA224 = "SHA224"
    HASH_SHA256 = "SHA256"
    HASH_SHA384 = "SHA384"
    HASH_SHA512 = "SHA512"

    CHOICES = [
        (HASH_SHA1, "SHA1", "red"),
        (HASH_SHA160, "SHA160", "orange"),
        (HASH_SHA224, "SHA224", "green"),
        (HASH_SHA256, "SHA256", "green"),
        (HASH_SHA384, "SHA384", "green"),
        (HASH_SHA512, "SHA512", "green"),
    ]


class CertKeyTypeChoices(ChoiceSet):
    TYPE_RSA = "RSA"
    TYPE_EC = "EC"
    TYPE_DSA = "DSA"

    CHOICES = [
        (TYPE_RSA, "RSA", "green"),
        (TYPE_EC, "EC", "green"),
        (TYPE_DSA, "DSA", "green"),
    ]


class CertBitLengthChoices(ChoiceSet):
    BITLENGTH_1024 = "1024"
    BITLENGTH_2048 = "2048"
    BITLENGTH_3072 = "3072"
    BITLENGTH_4096 = "4096"
    BITLENGTH_7680 = "7680"
    BITLENGTH_8192 = "8192"

    CHOICES = [
        (BITLENGTH_1024, "1024", "red"),
        (BITLENGTH_2048, "2048", "green"),
        (BITLENGTH_3072, "3072", "green"),
        (BITLENGTH_4096, "4096", "green"),
        (BITLENGTH_7680, "7680", "green"),
        (BITLENGTH_8192, "8192", "green"),
    ]


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
