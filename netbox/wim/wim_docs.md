


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
CPE
# DataSource - Disabled, Netbox already has a table named this in core/
OperatingSystem
Registrar - Deleting this in favor of a common Registrar/Vendor/Provider table
SiteLocation
SupportGroup - Unsure if using this
Vendor
WebEmail
# WebIPAddress - Disabled and attempting to use Netbox version in ipam/
WebserverFramework
```



Choices Objects:

```
DomainStatusChoices
FQDNStatusChoices
FQDNOpsStatusChoices
WebsiteOpsStatusChoices
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






## Initial Onboarding

To first start setting up this project as a new application, you need to start importing data to get going. Here are the first things you should import (because they are used by objects that get imported later in the sequence):


1. Tenant groups and Tenants
2. BusinessGroups (Groups first, so divisions can have a valid FK to them when imported next)
2. BusinessDivisions
3. Regions
4. Site Groups, and Sites (also SiteLocations for now)
    - For reference, pytz valid timezones: https://github.com/stub42/pytz/tree/master/tz
5. Manufacturers, Providers and/or Vendors
6. RIRs
7. ASNs
8. Platforms, OperatingSystems, WebserverFrameworks
9. Device Types, Roles
10. VRFs (Virtual Routing and Forwarding) - Create a general "Public Internet" one w/ no Tenant that our public subnets can fall into
11. IP/VLAN Roles
12. Prefixes, IP Ranges, and IP Addresses
13. VLANs
14. Domains
15. FQDNs









## Development - Full File Breakdown Explanations


project_root/



    netbox/

        templates/
            app/
                {files}.html        - The HTML templates for app pages




    app/
        api/        - For netbox, this is required for an app to function correctly, or views won't render, because data lookups are done via API calls.
            nested_serializers.py   - For ForeignKey references to get context behind a model's serializer. called by a serializer
            serializers.py          - A serializer of data when API calls are made.
            urls.py                 - Like the app urls.py file, but for the rest_framework's API router
            views.py                - Like the app views.py file, but for API definitions
        fields/                 - A fields file or directory is for custom model fields, like in cases where you want to create your own version of a CharField or IntegerField with different validation or something
            cpe.py              - Potential custom model field for CPE's

        forms/
            bulk_edit.py        - Define what models/fields can be bulk edited and how
            bulk_import.py      - Define what models/fields can be bulk imported and how
            filtersets.py       - The filters defined for the "Filters" view tab on list views
            model_forms.py      - Define the "edit" view for a particular model record
        management/
            commands/           - Create custom commands to use with manage.py
                update_domains.py   _ A custom created command
        migrations/             - All of this app's DB migrations
        models/                 - All of this app's DB models
        tables/
            {model_name}.py     - A table definition for a model that defines default columns, and fields that may be viewed in a table "list view". Linked to views.py as the defined table to use for the view.
        tests/
            test_models.py      - Basic app tests can go here, and are necessary if you wish to make a PR.
    

        apps.py         - Once you configure search.py, you will import it here to enable it for inclusion in the global search
        choices.py      - All choices definitions for CharField's that use choices in this app
        constants.py    - Any constants for the app (e.g. min/max port integers)
        filtersets.py   - This main app filtersets file is for filtering UI and API queries and every app has one.
        managers.py     - ipam uses this for a manager that sorts IP's in a better way
        querysets.py    - For really complicated/nested queryset definitions
        search.py       - Sets up indices on your models and fields you specify. Doesn't function on its own, other configurations are needed to make global search work, I believe this is in the apps.py file
        signals.py      - Handlers for post-save, pre-delete type actions
        urls.py         - App urls for routing, core file for all apps
        validators.py   - Custom validators to use in fields or forms, ensure good data is submitted. Caveat: the built-in URLValidator hates underscores...
        views.py        - Core app file, contains views that are configured in urls.py
        widgets.py      - Define custom form widgets for use in the app





### The global search feature


- The backend exists in /netbox/search/backends.py but doesn't contain too much code. It basically registers search for each enabled app into its global registry.


- Under netbox/forms/__init__.py, is the definition of the search form itself, and is where the code is at to setup the lookup choices, and preload the objects available from all of the apps


- Finally, the actual "view" for the Search is defined in netbox/netbox/views/misc.py as "SearchView".


- You can manually reindex all or a specific app using a manage.py custom command which is defined in netbox/extras/management/commands/reindex.py

```
python manage.py reindex <app>
# or, can only reindex if no cache already exists
python manage.py reindex <app> --lazy
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




#### Global Search

According to the docs, you just have to subclass SearchIndex, but when I did that it still was not working:
- https://docs.netbox.dev/en/stable/development/adding-models/




#### Dashboard Widgets

- Doc: https://docs.netbox.dev/en/stable/plugins/development/dashboard-widgets/

I'd suggest this page include some information on how to generate or use the "filters" form field when creating widgets in order to filter down the object lists or counts. It requires json, but not sure the exact syntax it must be.





#### For prefixes or ranges, add a link to arin whois lookup

This could be added as a <a>  link to the .html pages

```
"https://search.arin.net/rdap/?query={{ ip_range_here }}"

```







