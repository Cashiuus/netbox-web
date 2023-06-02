


Web Inventory Management (WIM)
==============================



## Notes on this Buildout

This all started as the culmination of many failed attempts at constructing a web property inventory & management system. On each occurrence,
I could build the database construct and populate it with data, but was unable to move past this phase of building an app and into the following key areas:
- Frontend that works - I mostly used Django Admin to work with the data, while doing bulk edits via import/export of CSV files.
- Task automation - Unable to get redis working, and 99% of "Django Tutorial for x" on the Internet is about blogging or static data websites with no automation features.
- A robust method of constructing "views" that allowed for customizing columns in view on the fly, tabs for data, and just an overall robust data table UI to present all of this data in a meaningful way.





### Model Definitions

Primary Asset Models:
```
Domain
FQDN
```


Supporting Models:

```
BusinessDivision
BusinessGroup
BusinessCriticality
CloudProvider
ComplianceProgram
CPE
# DataSource - Disabled, Netbox already has a table named this in core/
FqdnStatus
OperatingSystem
ParkedStatus
Registrar
SiteLocation
SupportGroup
Vendor
WebEmail
# WebIPAddress - Disabled and attempting to use Netbox version in ipam/
WebserverFramework
WebsiteAuthType
WebsiteStatus
```



Choices Objects:

```
DomainStatusChoices
FQDNStatusChoices

AssetClassChoices
RedirectStatusChoices
WebAuthChoices
WebsiteRoleChoices
```


Legacy Choices (Integers method):

```
RECORD_STATUS_CHOICES           # This was replaced (active, archive, delete, new)
INV_STATUS_CHOICES              # candidate, confirmed, rejected
ASSET_TYPE_CHOICES              # Not Used; asn, fqdn, ip_subnet
GEO_REGION_CHOICES              # global, amer, apac, emea
COMPLIANCE_CHOICES              # acronyms; replaced by DB table
CMDB_ARCH_MODEL                 # na, saas, onpremise, hybrid
HOSTING_ARCH_MODEL              # na, unk, saas, onpremise, cloud
FQDN_STATUS_CHOICES             # Not used
REDIRECT_STATUS_CHOICES         # Replaced this one
SITE_ENV_CHOICES                # Website Env (prod, qa, etc)
OS_ARCH_CHOICES                 # x86 or x64
LAYER_SECURITY_CHOICES          # TLS Protocol versions
CONFIDENCE_CHOICES              # candidate, confirmed, dismissed
IMPORTANCE_CHOICES              # unk, low, med, high, crit
SUPPORT_GROUP_TYPE_CHOICES      # Group types (e.g. SNOW, versus Team Name)
```










## Feedback for the Netbox Docs pages


- The development section could benefit from some clarity on the fact that you have to add the `--insecure` flag when running the Netbox locally for testing or it won't load. I'm not certain if this is a built-in function, but the `js` static media files won't load without it, causing the whole site to fail to load. I found this out by accident, but I don't think it was explicitly called out in the docs.




#### API Issues


- Ref docs: https://docs.netbox.dev/en/stable/plugins/development/rest-api/

The example here is missing the app_name?

How do we get our app api into the namespace?

File: wim/api/urls.py
```
app_name = "wim-api"
```