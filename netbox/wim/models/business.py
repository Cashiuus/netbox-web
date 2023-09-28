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
    'Brand',
    'BusinessCriticality',
    'BusinessDivision',
    'BusinessGroup',
    'SiteLocation',
    'SupportGroup',
)


# ---------------------
# Business Objects
# ---------------------

class Brand(OrganizationalModel):
    """
    A Brand is a major brand, segment, acquisition, or recognizable component
    of the company to which it's important to attribute assets.
    """
    # OrganizationalModel class automatically comes with: name, slug, description

    # notes = models.TextField(_('Notes'), blank=True, default='',
    #                          help_text='Notable remarks about this division, such as brand names associated')
    date_created = models.DateTimeField(_('Date Created'), auto_now_add=True,
                                        help_text='system field for creation date')
    date_modified = models.DateTimeField(_('Date Modified'), auto_now=True,
                                         help_text='system field for modified date')

    class Meta:
        ordering = ['name']
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wim:brand', args=[self.pk])


class BusinessCriticality(OrganizationalModel):
    """
    A basic tier system for business criticality to categorize asset
    importance to the business
    """
    name = models.CharField(_('Name'), max_length=50, unique=True)
    description = models.CharField(_('Description'), max_length=150)
    order = models.SmallIntegerField(default=10)
    color = ColorField(
        default=ColorChoices.COLOR_GREY
    )

    class Meta:
        ordering = ('order', 'name',)
        verbose_name = _('Business Criticality')
        verbose_name_plural = _('Business Criticalities')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wim:businesscriticality', kwargs=[self.pk])


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
        unique=True,
        help_text='Abbrev. name of the business group'
    )
    principal_location_orig = models.ForeignKey(
        'wim.SiteLocation',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='+',
        verbose_name='Principal Location Mine',
    )
    principal_location_nb = models.ForeignKey(
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

    def get_absolute_url(self):
        return reverse('wim:businessgroup', args=[self.pk])
        # return reverse('wim:businessgroup', kwargs={'pk': self.pk})


class BusinessDivision(OrganizationalModel):
    """
    A division that resides under a particular Group in the org hierarchy.
    This is 2nd level grouping (Company -> Group -> Division).
    """
    name = models.CharField(_('Name'), max_length=100, unique=True)
    acronym = models.CharField(_('Acronym'), max_length=10, unique=True)
    group = models.ForeignKey('BusinessGroup', on_delete=models.CASCADE,
                              verbose_name='Group')
    principal_location_orig = models.ForeignKey('SiteLocation', on_delete=models.SET_NULL, blank=True, null=True)
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

    def get_absolute_url(self):
        return reverse('wim:businessdivision', args=[self.pk])
        # return reverse('wim:businessdivision', kwargs={'pk': self.pk})


class SupportGroup(OrganizationalModel):
    """
    A support group or defined "Team" responsible for an asset that can be assigned.
    """
    name = models.CharField(_('Group Name'), max_length=255, unique=True,
                            help_text='SNOW group name or App Team Name')
    description = models.TextField(_('Description'), blank=True)
    group_type_int = models.IntegerField(
        _('Geo Region'),
        choices=SUPPORT_GROUP_TYPE_CHOICES,
        default=SUPPORT_GROUP_TYPE_CHOICES.servicenow,
        help_text='Is this an official group name for ticketing or just a team name'
    )
    # TODO: I can infer group from a selected division at some point because they
    # are already linked there.
    group_orig = models.ForeignKey('BusinessGroup', on_delete=models.CASCADE)
    division_orig = models.ForeignKey('BusinessDivision', on_delete=models.CASCADE)
    group_members_orig = models.TextField(_('Group Members'), blank=True, default='',
                                     help_text='List all members of the group')
    group_leader_orig = models.CharField(_('Group Leader'), max_length=255, blank=True, default='',
                                    help_text='Group leader or highest ranking executive')

    # TODO: Not sure how i want to structure owners just yet
    #owner = models.ForeignKey('Person', on_delete=models.PROTECT)
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

    def get_absolute_url(self):
        return reverse('wim:supportgroup', kwargs=[self.pk])


class SiteLocation(OrganizationalModel):
    """
    Phsyical (or Digital) sites or site codes to which an asset or support team may belong.
    This is similar to NetBox's "Site" table, but using this for now until a firm path is chosen.
    """
    code = models.CharField(_('Site Code'), max_length=20, unique=True)
    name = models.CharField(_('Name'), max_length=255, help_text='Brief name of the site or location')
    slug = models.SlugField(max_length=100, unique=True)
    active = models.BooleanField(
        default=True,
        verbose_name='Active',
        help_text=_('Location is active or inactive (closed)')
    )
    priority = models.PositiveSmallIntegerField(
        _('Priority'),
        default=50,
        help_text='Prioritization scoring of site locations (higher score = more critical)'
    )
    impacted_group_orig = models.ForeignKey(
        'BusinessGroup',
        on_delete=models.CASCADE,
        blank=True, null=True,
    )
    impacted_division_orig = models.ForeignKey(
        'BusinessDivision',
        on_delete=models.CASCADE,
        blank=True, null=True,
    )
    street = models.CharField(_('Street'), max_length=255, blank=True, default='')
    city = models.CharField(_('city'), max_length=50, blank=True, default='')
    state = models.CharField(_('State/Region'), max_length=50, blank=True, default='')
    country_1 = models.CharField(_('Country Code'), max_length=5, default='US')
    # Note: This won't work if countries we want to import aren't in our choices
    # country = CountryField()
    geo_region_choice = models.CharField(
        max_length=50,
        choices=GeoRegionChoices,
        blank=True,
    )
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
        help_text=_("GPS coordinate in decimal format (xx.yyyyyy)"),
    )
    it_infra_contact = models.CharField(
        _('IT Infra POC'),
        max_length=255,
        blank=True, default='',
        help_text=_('Primary Site IT Infrastructure Point of Contact'),
    )
    approx_network_size = models.IntegerField(_('Approx Network Size'), blank=True, null=True)
    ranges_tmp1 = models.TextField(
        _('Network Ranges'),
        blank=True, default='',
        help_text='Known ranges from netinfo',
    )
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
        # return reverse('wim:sitelocation', args=[self.pk])
        return reverse('wim:sitelocation', args=[self.pk])


# class ComplianceProgram(OrganizationalModel):
#     """ A compliance/regulation program under which a web application or server may be subject. """
#     name = models.CharField(_('Name'), max_length=255, unique=True)
#     acronym = models.CharField(_('Acronym'), max_length=15, unique=True)
#     description = models.TextField(_('Description'))
#     website = models.URLField(_('Website'), blank=True, null=True)
#     mandates_pentesting_orig = models.BooleanField(_('Mandates Pentests'), null=True, default=False)
#     mandates_vulnscanning_orig = models.BooleanField(_('Mandates Vuln Scans'), null=True, default=True)
#     # originating_country = CountryField(_('Country'))

#     # TODO: Future use may include fields for dot notation directive numbers or reference maps
#     # like is done with NIST CSR and like frameworks to map requirements across programs for similar
#     # defense techniques or checks

#     order = models.SmallIntegerField(default=10)

#     class Meta:
#         ordering = ('acronym',)
#         verbose_name = _('compliance program')
#         verbose_name_plural = _('compliance programs')

#     def __str__(self):
#         return self.acronym

#     def get_absolute_url(self):
#         return reverse('wim:complianceprogram', kwargs={'pk': self.pk})

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
