from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from timezone_field import TimeZoneField

from netbox.models import OrganizationalModel, PrimaryModel
from utilities.choices import ColorChoices
from utilities.fields import ColorField, NaturalOrderingField
from wim.choices import *


__all__ = (
    'BusinessDivision',
    'BusinessGroup',
    'BusinessCriticality',
    'CloudProvider',
    'ComplianceProgram',
    # 'DataSource',
    'FqdnStatus',
    'OperatingSystem',
    'ParkedStatus',
    'SiteLocation',
    'SupportGroup',
    'WebserverFramework',
    'WebsiteAuthType',
    'WebsiteStatus',
)

# class AssetClass(OrganizationalModel):
#     """ 
#     Primary classficiation types for assets in our inventory 
#     (Domain, FQDN, Server, etc). 
#     """
#     name = models.CharField(
#         _('Type'), 
#         max_length=100, 
#         unique=True,
#         help_text='An asset type category'
#     )
#     slug = models.SlugField(max_length=100)
#     # order = models.SmallIntegerField(default=10)
#     # color = models.CharField(max_length=20, default="#FF0000")

#     class Meta:
#         #default_manager_name =
#         ordering = ['name']
#         verbose_name = _('Asset Class')
#         verbose_name_plural = _('Asset Classes')

#     def __str__(self):
#         return self.name
    


class FqdnStatus(OrganizationalModel):
    """ A basic operational status for FQDNs. """
    name = models.CharField(_('Name'), max_length=50, unique=True)
    description = models.TextField(_('Description'))
    order = models.SmallIntegerField(default=10)
    color = ColorField(
        default=ColorChoices.COLOR_GREY
    )
    # color = models.CharField(max_length=20, default="#FF0000")

    class Meta:
        ordering = ('order', 'name')
        verbose_name = _('FQDN Status')
        verbose_name_plural = _('FQDN Statuses')

    def __str__(self):
        return self.name


class WebsiteStatus(OrganizationalModel):
    """ A basic operational status for Live Websites. """
    name = models.CharField(_('Name'), max_length=50, unique=True)
    description = models.TextField(_('Description'))
    order = models.SmallIntegerField(default=10)
    color = ColorField(
        default=ColorChoices.COLOR_GREY
    )
    # color = models.CharField(max_length=20, default="#FF0000")

    class Meta:
        ordering = ('order', 'name')
        verbose_name = _('Website Status')
        verbose_name_plural = _('Website Statuses')

    def __str__(self):
        return self.name


class ParkedStatus(OrganizationalModel):
    """ A parked (301/302) status for FQDNs, separating if we are handling the park or if its a 3rd party. """
    name = models.CharField(_('Name'), max_length=50, unique=True)
    description = models.TextField(_('Description'))
    order = models.SmallIntegerField(default=10)
    color = ColorField(
        default=ColorChoices.COLOR_GREY
    )
    # color = models.CharField(max_length=20, default="#FF0000")

    class Meta:
        ordering = ('order', 'name')
        verbose_name = _('Parked Status')
        verbose_name_plural = _('Parked Statuses')

    def __str__(self):
        return self.name


class WebserverFramework(OrganizationalModel):
    """ Data sources that will feed this CMDB, so we can mark where data came from. """
    name = models.CharField(
        _('Name'), 
        max_length=50, 
        unique=True,
        help_text='The name and version of the server framework (e.g. Apache/2.4.9)'
    )
    product = models.CharField(_('product'), max_length=250, blank=True, default='')
    version = models.CharField(_('version'), max_length=50, blank=True, default='')
    cpe = models.ForeignKey(
        to='wim.CPE',
        on_delete=models.PROTECT,
        related_name='webserver_frameworks',
        blank=True,
        verbose_name='CPE'
    )
    order = models.SmallIntegerField(default=10)
    # color = models.CharField(max_length=20, default="#FF0000")
    notes = models.TextField(_('Notes'), blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Webserver Framework')
        verbose_name_plural = _('Webserver Frameworks')

    def __str__(self):
        return self.name
        #return '{0}/{1}'.format(self.product, self.version)



class WebsiteAuthType(OrganizationalModel):
    """ FK for categories of authentication methods. """
    name = models.CharField(
        _('Auth Type'), 
        max_length=100, 
        unique=True,
        help_text='An authentication method for use in fingerprinting website features'
    )
    order = models.SmallIntegerField(default=10)
    # color = models.CharField(max_length=20, default="#FF0000")

    class Meta:
        #default_manager_name =
        ordering = ['name']
        verbose_name = _('Auth Type')
        verbose_name_plural = _('Auth Types')

    def __str__(self):
        return self.name
    

class CloudProvider(OrganizationalModel):
    """ A list of cloud providers and useful data for each. """
    name = models.CharField(_('Name'), max_length=75, unique=True)
    description = models.TextField(_('Description'), blank=True)
    testing_reqs = models.TextField(_('Testing Requirements'), blank=True,
                                    help_text='List instructions or approvals this vendor requires before authorizing pentesting')

    def __str__(self):
        return self.name


# class DataSource(OrganizationalModel):
#     """ Data sources that will feed this CMDB, so we can mark where data came from. """
#     name = models.CharField(_('Name'), max_length=50, unique=True)
#     #logo =
#     description = models.CharField(_('Description'), max_length=150)
#     order = models.SmallIntegerField(default=10)
#     # color = models.CharField(max_length=20, default="#FF0000")
#     color = ColorField(
#         default=ColorChoices.COLOR_GREY
#     )

#     class Meta:
#         ordering = ('name',)
#         verbose_name = _('Data Source')
#         verbose_name_plural = _('Data Sources')

#     def __str__(self):
#         return self.name

# ========[ Miscellaneous CMDB Type Lists ]========= #
class OperatingSystem(OrganizationalModel):
    """
        A selection of operating system definitions to be used with Assets.
    """
    vendor = models.CharField(_('Vendor'), max_length=100)
    product = models.CharField(_('Name'), max_length=100)
    family = models.CharField(_('Family'), max_length=100, blank=True,
                              help_text='Grouping OS together, such as Linux and Windows')
    update = models.CharField(_('Service Pack'), max_length=10, blank=True,
                              help_text='Revision or Service Pack value')
    build = models.CharField(_("OS Build"), max_length=50, blank=True)
    cpe = models.OneToOneField(
        to='wim.CPE',
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        verbose_name='CPE'
    )
    color = ColorField(
        default=ColorChoices.COLOR_GREY
    )

    class Meta:
        ordering = ['vendor', 'product']
        unique_together = ['vendor', 'product', 'update']
        verbose_name = _('operating system')
        verbose_name_plural = _('operating systems')

    def __str__(self):
        return u'%s %s %s' % (self.vendor, self.product, self.update)



class ComplianceProgram(OrganizationalModel):
    """ A compliance/regulation program under which a web application or server may be subject. """
    name = models.CharField(_('Name'), max_length=255, unique=True)
    acronym = models.CharField(_('Acronym'), max_length=15, unique=True)
    description = models.TextField(_('Description'))
    website = models.URLField(_('Website'), blank=True, null=True)
    mandates_pentesting_9 = models.BooleanField(_('Mandates Pentests'), null=True, default=False)
    mandates_vulnscanning_9 = models.BooleanField(_('Mandates Vuln Scans'), null=True, default=True)
    # originating_country = CountryField(_('Country'))

    # TODO: Future use may include fields for dot notation directive numbers or reference maps
    # like is done with NIST CSR and like frameworks to map requirements across programs for similar
    # defense techniques or checks

    order = models.SmallIntegerField(default=10)

    class Meta:
        ordering = ('acronym',)
        verbose_name = _('compliance program')
        verbose_name_plural = _('compliance programs')

    def __str__(self):
        return self.acronym





# ---------------------
# Business Objects
# ---------------------

class BusinessGroup(OrganizationalModel):
    """
        A business group, for orgs that are split into these at the top level of org.
        This is first level grouping (Company -> Group).
    """
    name = models.CharField(
        _('Name'), 
        max_length=100, 
        unique=True, 
        help_text='Full name of the business group'
    )
    acronym = models.CharField(
        _('Acronym'), 
        max_length=10, 
        help_text='Abbrev. name of the business group'
    )
    principal_location_9 = models.ForeignKey(
        'wim.SiteLocation', 
        on_delete=models.SET_NULL, 
        blank=True, null=True,
        related_name='+',
        verbose_name='Principal Location Mine',
    )
    principal_location_8 = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='+',
        verbose_name='Principal Location NB',

    )
    description = models.TextField(_('Description'), blank=True)
    # notes = models.TextField(_('Notes'), 
    #                          blank=True,
    #                          help_text='Notable remarks about this business group, such as brand names associated')
    date_created = models.DateTimeField(_('Date Created'), 
                                        auto_now_add=True,
                                        help_text='system field for creation date')
    date_modified = models.DateTimeField(_('Date Modified'),
                                         auto_now=True, 
                                         help_text='system field for modified date')

    class Meta:
        ordering = ['acronym']
        verbose_name = _('Business Group')
        verbose_name_plural = _('Business Groups')

    def __str__(self):
        return self.acronym


class BusinessDivision(OrganizationalModel):
    """ A division that resides under a particular Group in the org hierarchy.
        This is 2nd level grouping (Company -> Group -> Division).
    """
    name = models.CharField(_('Name'), max_length=100)
    acronym = models.CharField(_('Acronym'), max_length=10)
    group = models.ForeignKey('BusinessGroup', on_delete=models.CASCADE,
                              verbose_name='Group')
    principal_location = models.ForeignKey('SiteLocation', on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, default='')
    # notes = models.TextField(_('Notes'), blank=True, default='',
    #                          help_text='Notable remarks about this division, such as brand names associated')
    date_created = models.DateTimeField(_('Date Created'), auto_now_add=True,
                                        help_text='system field for creation date')
    date_modified = models.DateTimeField(_('Date Modified'), auto_now=True,
                                         help_text='system field for modified date')

    class Meta:
        ordering = ['acronym']
        verbose_name = _('Business Division')
        verbose_name_plural = _('Business Divisions')

    def __str__(self):
        return self.acronym


class SupportGroup(OrganizationalModel):
    name = models.CharField(_('Group Name'), max_length=255, unique=True,
                            help_text='SNOW group name or App Team Name')
    description = models.TextField(_('Description'), blank=True)

    group_type = models.IntegerField(_('Geo Region'),
                                     choices=SUPPORT_GROUP_TYPE_CHOICES,
                                     default=SUPPORT_GROUP_TYPE_CHOICES.servicenow,
                                     help_text='Is this an official group name for ticketing or just a team name')

    # TODO: I can infer group from a selected division at some point because they are already linked there.
    group = models.ForeignKey('BusinessGroup', on_delete=models.CASCADE)
    division = models.ForeignKey('BusinessDivision', on_delete=models.CASCADE)

    group_members = models.TextField(_('Group Members'), blank=True, default='',
                                     help_text='List all members of the group')

    group_leader = models.CharField(_('Group Leader'), max_length=255, blank=True, default='',
                                    help_text='Group leader or highest ranking executive')

    #owner = models.ForeignKey('Person', on_delete=models.PROTECT)
    # TODO: not sure how i want to structure owners just yet.
    #website_manager = models.CharField(_('Website Manager'), blank=True, default='')
    #website_developer = models.CharField(_('Website Developer'), blank=True, default='')

    # notes = models.TextField(_('Notes'), blank=True)
    date_created = models.DateTimeField(_('Date Created'), auto_now_add=True,
                                        help_text='system field for creation date')
    date_modified = models.DateTimeField(_('Date Modified'), auto_now=True,
                                         help_text='system field for modified date')

    class Meta:
        ordering = ('name',)
        verbose_name = _('Support Group')
        verbose_name_plural = _('Support Groups')
        #indexes = [
        #    models.Index(fields=['website_manager', 'website_developer']),
        #]

    def __str__(self):
        return self.name


class BusinessCriticality(OrganizationalModel):
    """ A basic tier system for business criticality to categorize assets by. """
    name = models.CharField(_('Name'), max_length=50, unique=True)
    description = models.CharField(_('Description'), max_length=150)
    order = models.SmallIntegerField(default=10)
    color = ColorField(
        default=ColorChoices.COLOR_GREY
    )
    # color = models.CharField(max_length=20, default="#FF0000")

    class Meta:
        ordering = ('order', 'name',)
        verbose_name = _('Business Criticality')
        verbose_name_plural = _('Business Criticalities')

    def __str__(self):
        return self.name


class SiteLocation(OrganizationalModel):
    """ 
    Digital sites or site codes to which an asset or support team may belong. 
    """
    code = models.CharField(_('Site Code'), max_length=10, unique=True)
    name = models.CharField(_('Name'), max_length=255, help_text='Brief name of the site or location')
    slug = models.SlugField(max_length=100, unique=True)
    priority = models.PositiveSmallIntegerField(
        _('Priority'), 
        default=50, 
        help_text='Prioritization scoring of site locations (higher score = more critical)'
    )
    impacted_group = models.ForeignKey('BusinessGroup',
                                       on_delete=models.CASCADE, blank=True, null=True)
    impacted_division = models.ForeignKey('BusinessDivision',
                                          on_delete=models.CASCADE, blank=True, null=True)
    street = models.CharField(_('Street'), max_length=255, blank=True, default='')
    city = models.CharField(_('city'), max_length=50, blank=True, default='')
    state = models.CharField(_('State/Region'), max_length=50, blank=True, default='')
    country_1 = models.CharField(_('Country Code'), max_length=5, default='US')
    # country = CountryField()        # Note: This won't work if countries we want to import aren't in our choices
    geo_region_9 = models.IntegerField(_('Region'),
                                     choices=GEO_REGION_CHOICES,
                                     default=GEO_REGION_CHOICES.amer)
    
    geo_region = models.ForeignKey(
        to='dcim.Region',
        on_delete=models.SET_NULL,
        related_name="sitelocations",
        blank=True, null=True,
        verbose_name="Region",
    )

    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='sitelocations',
        blank=True, null=True,
    )

    contacts = GenericRelation(
        to='tenancy.ContactAssignment'
    )

    timezone_1 = models.CharField(_('Timezone'), max_length=50, blank=True, default='')
    timezone = TimeZoneField(blank=True)

    latitude = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        blank=True,
        null=True,
        help_text=_("GPS coordinate in decimal format (xx.yyyyyy)")
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        help_text=_("GPS coordinate in decimal format (xx.yyyyyy)")
    )

    it_infra_contact = models.CharField(
        _('IT Infra POC'), 
        max_length=255, 
        blank=True, default='',
        help_text='Primary Site IT Infrastructure Point of Contact'
    )
    approx_network_size = models.IntegerField(_('Approx Network Size'), blank=True, null=True)
    ranges_tmp1 = models.TextField(_('Network Ranges'), blank=True, default='',
                                   help_text='Known ranges from netinfo')
    asns = models.ManyToManyField(
        to='ipam.ASN',
        related_name='sitelocations',
        blank=True,
    )
    notes = models.TextField(_('Notes'), blank=True, default='')

    class Meta:
        ordering = ('code',)
        verbose_name = _('Site Location')
        verbose_name_plural = _('Site Locations')

    def __str__(self):
        return self.code
    
    def get_absolute_url(self):
        return reverse('wim:sitelocation', args=[self.pk])
