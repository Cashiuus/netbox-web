from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from dcim.models import Device, Interface, Location, Platform, Rack, Region, Site, SiteGroup
# from ipam.choices import *
# from ipam.constants import *
from ipam.formfields import IPNetworkFormField
from ipam.models import *
from netbox.forms import NetBoxModelForm
from tenancy.forms import TenancyForm
from utilities.exceptions import PermissionsViolation
from utilities.forms import BootstrapMixin, add_blank_choice
from utilities.forms.fields import (
    CommentField, ContentTypeChoiceField, DynamicModelChoiceField, DynamicModelMultipleChoiceField, NumericArrayField,
    SlugField,
)
from utilities.forms.widgets import DatePicker
# from dcim.models import Platform
# from ipam.models import IPAddress
from wim.models import *


__all__ = (
    'DomainForm',
    'FQDNForm',
    'BusinessDivisionForm',
    'BusinessGroupForm',
    'OperatingSystemForm',
)


class DomainForm(TenancyForm, NetBoxModelForm):
    # FKs
    # registrar_company = DynamicModelChoiceField(
    #     queryset=Registrar.objects.all(),
    #     required=True,
    #     selector=True,
    # )

    # fieldsets = (
    # )
    
    class Meta:
        model = Domain
        fields = [
            'name', 'status_9', 'status', 
            'confidence', 'meets_standards',
            'tenant',
            'date_registrar_expiry', 'date_first_registered',
            'date_last_recon_scanned',
            'is_internet_facing', 'is_flagship',
            'registrar_company_9', 'registrar_iana_id_9',
            'registrar_domain_statuses',
            'registrant_org',
            'registration_emails_9', 'registration_emails',
            'nameservers', 'mail_servers', 'whois_servers',
            'soa_nameservers', 'soa_email',
            'notes',
        ]


class FQDNForm(TenancyForm, NetBoxModelForm):
    # FKs
    # fqdn_status = DynamicModelChoiceField(
    #     queryset=FqdnStatus.objects.all(),
    #     required=True,
    #     selector=True,
    # )
    # website_status = DynamicModelChoiceField(
    #     queryset=WebsiteStatus.objects.all(),
    #     required=False,
    #     selector=True,
    # )
    domain = DynamicModelChoiceField(
        queryset=Domain.objects.all(),
        required=True,
        selector=True,
    )
    # ipaddress_public_8 = DynamicModelChoiceField(
    #     queryset=IPAddress.objects.all(),
    #     required=False,
    #     selector=True,
    # )
    # ipaddress_private_8 = DynamicModelChoiceField(
    #     queryset=IPAddress.objects.all(),
    #     required=False,
    #     selector=True,
    # )
    ipaddress_public_8 = IPNetworkFormField(required=False)
    ipaddress_private_8 = IPNetworkFormField(required=False)
    # os_1 = DynamicModelChoiceField(
    #     queryset=OperatingSystem.objects.all(),
    #     required=False,
    #     selector=True,
    #     label=_("OS_v1")
    # )
    os_8 = DynamicModelChoiceField(
        queryset=Platform.objects.all(),
        required=False,
        selector=True,
        label=_('OS_8')
    )
    # impacted_group_9 = DynamicModelChoiceField(
    #     queryset=BusinessGroup.objects.all(),
    #     required=False,
    #     selector=True,
    # )
    # impacted_division_9 = DynamicModelChoiceField(
    #     queryset=BusinessDivision.objects.all(),
    #     required=False,
    #     selector=True,
    # )
    # location_9 = DynamicModelChoiceField(
    #     queryset=SiteLocation.objects.all(),
    #     required=False,
    #     selector=True,
    # )
    location = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        # initial_params={
        #     "location": "$location"
        # },
        # query_params={
        #     "region_id": "$region",
        #     "group_id": "$sitegroup",
        # }
    )
    geo_region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        # initial_params={
        #     "sites": 
        # }
    )
    # cloud_provider_9 = DynamicModelChoiceField()
    # snow_bcdr_criticality = DynamicModelChoiceField(
    #     queryset=BusinessCriticality.objects.all(),
    #     required=False,
    # )
    # tech_webserver_1 = DynamicModelChoiceField(
    #     queryset=WebserverFramework.objects.all(),
    #     required=False,
    # )

    # parked_status = DynamicModelChoiceField()

    # vendor_company_1 = DynamicModelChoiceField(
    #     queryset=Vendor.objects.all(),
    #     required=False,
    # )

    # TODO: Make this choices instead of a FK
    # feature_auth_type = DynamicModelChoiceField(
    #     queryset=WebsiteAuthType.objects.all(),
    #     required=False,
    # )

    # M2M
    # compliance_programs = DynamicModelMultipleChoiceField(
    #     queryset=ComplianceProgram.objects.all(),
    #     required=False,
    # )

    # Booleans
    is_compliance_required = forms.BooleanField(
        required=False,
        label=_('Is Compliance Required')
    )
    tls_cert_is_wildcard = forms.BooleanField(required=False)

    is_internet_facing = forms.BooleanField(required=False)
    is_flagship = forms.BooleanField(required=False)
    is_cloud_hosted = forms.BooleanField(required=False)
    is_vendor_managed = forms.BooleanField(required=False)
    is_vendor_hosted = forms.BooleanField(required=False)

    is_akamai = forms.BooleanField(required=False)
    is_load_protected = forms.BooleanField(required=False)
    is_waf_protected = forms.BooleanField(required=False)
    is_vhost = forms.BooleanField(required=False)
    is_http2 = forms.BooleanField(required=False)

    had_bugbounty = forms.BooleanField(required=False)
    is_riskey = forms.BooleanField(required=False)

    fieldsets = (
        ("FQDN", (
            "name", "status_9", "status", "fqdn_status", "website_status"
            'env_used_for_1', 'architectural_model_1', 
            "geo_region_9", "geo_region",
            "location_9", "location",
            "domain", "asset_class",
            'criticality_score_1', 'snow_bcdr_criticality',

        )),
        ("Tenancy", (
            "impacted_group_9", "impacted_division_9",
            "owners_9", "tenant",
            'support_group_website_technical', 'support_group_website_approvals',
            "is_in_cmdb", 'is_internet_facing', 'is_flagship',

        )),
        ("Technical Details", (
            'website_url', 'website_title', 'website_email', 'role',
            'site_operation_age',
            "public_ip_9", "ipaddress_public_8",
            'tech_webserver_1', 'tech_addtl',
            'redirect_health', 'redirect_url', 'redirect_status_9',
            'private_ip_9', 'ipaddress_private_8', 'hostname_9',
            'os_9', 'os_1', 'os_8',
        )),
        ("Security", (
            'had_bugbounty', 'is_risky',
            'vuln_scan_coverage', 'vuln_scan_last_date',
            'last_vuln_assessment', 'vuln_assessment_priority',
            'risk_analysis_notes',
        )),
        ("Scoping", (
            'is_akamai', 'is_load_protected', 'is_waf_protected',
            'feature_api',
            'feature_acct_mgmt', 'feature_auth_type', 'feature_auth_self_registration',
            'scoping_size', 'scoping_complexity', 'scoping_roles',
            'is_compliance_required', 'compliance_programs',
        )),
        ("TLS", (
            'tls_version', 'tls_cert_expires',
            'tls_cert_info', 'tls_cert_sha1', 'tls_cert_is_wildcard',
        )),
        ("Vendor", (
            'vendor_company_1', 'vendor_pocs_9', 'vendor_notes',
        )),
        ("", (
            "notes", "tags",
        ))
    )

    class Meta:
        model = FQDN
        fields = [
            'name', 'status_9', 'status', 'fqdn_status', 'website_status',
            'domain', 'asset_class', 
            'impacted_group_9', 'impacted_division_9',
            'location_9', 'location',
            'geo_region_9', 'geo_region',
            'env_used_for_1', 'architectural_model_1', 
            'tech_webserver_1', 'tech_addtl',
            'is_in_cmdb',
            'public_ip_9', 'ipaddress_public_8',
            'tenant', 'owners_9',
            'support_group_website_technical', 'support_group_website_approvals',
            'private_ip_9', 'ipaddress_private_8', 'hostname_9',
            'os_9', 'os_1', 'os_8',
            'criticality_score_1', 'snow_bcdr_criticality',
            'tls_version', 'tls_cert_expires',
            'tls_cert_info', 'tls_cert_sha1', 'tls_cert_is_wildcard',
            'website_url', 'website_title', 'website_email', 'role',
            'site_operation_age',
            'redirect_health', 'redirect_url', 'redirect_status_9',
            'had_bugbounty', 'is_risky',
            'vuln_scan_coverage', 'vuln_scan_last_date',
            'last_vuln_assessment', 'vuln_assessment_priority',
            'risk_analysis_notes',
            'is_internet_facing', 'is_flagship',
            'cloud_provider_9',
            'is_vendor_managed', 'is_vendor_hosted',
            'vendor_company_1', 'vendor_pocs_9',
            'vendor_notes',
            'is_akamai', 'is_load_protected', 'is_waf_protected',
            'feature_api',
            'feature_acct_mgmt', 'feature_auth_type', 'feature_auth_self_registration',
            # Scoping --
            'scoping_size', 'scoping_complexity', 'scoping_roles',
            'is_compliance_required', 'compliance_programs',
            'notes',
            'tags',
        ]



class BusinessGroupForm(NetBoxModelForm):

    class Meta:
        model = BusinessGroup
        fields = ['name', 'acronym']



class BusinessDivisionForm(NetBoxModelForm):

    class Meta:
        model = BusinessDivision
        fields = ['name', 'acronym']



class OperatingSystemForm(NetBoxModelForm):

    class Meta:
        model = OperatingSystem
        fields = ['vendor', 'product', 'update']







# class RoleForm(NetBoxModelForm):
#     slug = SlugField()

#     fieldsets = (
#         ('Role', (
#             'name', 'slug', 'weight', 'description', 'tags',
#         )),
#     )

#     class Meta:
#         model = Role
#         fields = [
#             'name', 'slug', 'weight', 'description', 'tags',
#         ]




# class ASNForm(TenancyForm, NetBoxModelForm):
#     rir = DynamicModelChoiceField(
#         queryset=RIR.objects.all(),
#         label=_('RIR'),
#     )
#     sites = DynamicModelMultipleChoiceField(
#         queryset=Site.objects.all(),
#         label=_('Sites'),
#         required=False
#     )
#     comments = CommentField()

#     fieldsets = (
#         ('ASN', ('asn', 'rir', 'sites', 'description', 'tags')),
#         ('Tenancy', ('tenant_group', 'tenant')),
#     )

#     class Meta:
#         model = ASN
#         fields = [
#             'asn', 'rir', 'sites', 'tenant_group', 'tenant', 'description', 'comments', 'tags'
#         ]
#         widgets = {
#             'date_added': DatePicker(),
#         }

#     def __init__(self, data=None, instance=None, *args, **kwargs):
#         super().__init__(data=data, instance=instance, *args, **kwargs)

#         if self.instance and self.instance.pk is not None:
#             self.fields['sites'].initial = self.instance.sites.all().values_list('id', flat=True)

#     def save(self, *args, **kwargs):
#         instance = super().save(*args, **kwargs)
#         instance.sites.set(self.cleaned_data['sites'])
#         return instance



# class IPRangeForm(TenancyForm, NetBoxModelForm):
#     vrf = DynamicModelChoiceField(
#         queryset=VRF.objects.all(),
#         required=False,
#         label=_('VRF')
#     )
#     role = DynamicModelChoiceField(
#         queryset=Role.objects.all(),
#         required=False
#     )
#     comments = CommentField()

#     fieldsets = (
#         ('IP Range', ('vrf', 'start_address', 'end_address', 'role', 'status', 'mark_utilized', 'description', 'tags')),
#         ('Tenancy', ('tenant_group', 'tenant')),
#     )

#     class Meta:
#         model = IPRange
#         fields = [
#             'vrf', 'start_address', 'end_address', 'status', 'role', 'tenant_group', 'tenant', 'mark_utilized',
#             'description', 'comments', 'tags',
#         ]


# class IPAddressForm(TenancyForm, NetBoxModelForm):
#     interface = DynamicModelChoiceField(
#         queryset=Interface.objects.all(),
#         required=False,
#         selector=True,
#     )
#     primary_for_parent = forms.BooleanField(
#         required=False,
#         label=_('Make this the primary IP for the device/VM')
#     )
#     comments = CommentField()

#     class Meta:
#         model = IPAddress
#         fields = [
#             'address', 'vrf', 'status', 'role', 'dns_name', 'primary_for_parent', 'nat_inside', 'tenant_group',
#             'tenant', 'description', 'comments', 'tags',
#         ]

#     def __init__(self, *args, **kwargs):

#         # Initialize helper selectors
#         instance = kwargs.get('instance')
#         initial = kwargs.get('initial', {}).copy()
#         if instance:
#             if type(instance.assigned_object) is Interface:
#                 initial['interface'] = instance.assigned_object
#             elif type(instance.assigned_object) is VMInterface:
#                 initial['vminterface'] = instance.assigned_object
#             elif type(instance.assigned_object) is FHRPGroup:
#                 initial['fhrpgroup'] = instance.assigned_object
#         kwargs['initial'] = initial

#         super().__init__(*args, **kwargs)

#         # Initialize primary_for_parent if IP address is already assigned
#         if self.instance.pk and self.instance.assigned_object:
#             parent = getattr(self.instance.assigned_object, 'parent_object', None)
#             if parent and (
#                 self.instance.address.version == 4 and parent.primary_ip4_id == self.instance.pk or
#                 self.instance.address.version == 6 and parent.primary_ip6_id == self.instance.pk
#             ):
#                 self.initial['primary_for_parent'] = True

#     def clean(self):
#         super().clean()

#         # Handle object assignment
#         selected_objects = [
#             field for field in ('interface', 'vminterface', 'fhrpgroup') if self.cleaned_data[field]
#         ]
#         if len(selected_objects) > 1:
#             raise forms.ValidationError({
#                 selected_objects[1]: "An IP address can only be assigned to a single object."
#             })
#         elif selected_objects:
#             self.instance.assigned_object = self.cleaned_data[selected_objects[0]]
#         else:
#             self.instance.assigned_object = None

#         # Primary IP assignment is only available if an interface has been assigned.
#         interface = self.cleaned_data.get('interface') or self.cleaned_data.get('vminterface')
#         if self.cleaned_data.get('primary_for_parent') and not interface:
#             self.add_error(
#                 'primary_for_parent', "Only IP addresses assigned to an interface can be designated as primary IPs."
#             )

#         # Do not allow assigning a network ID or broadcast address to an interface.
#         if interface and (address := self.cleaned_data.get('address')):
#             if address.ip == address.network:
#                 msg = f"{address} is a network ID, which may not be assigned to an interface."
#                 if address.version == 4 and address.prefixlen not in (31, 32):
#                     raise ValidationError(msg)
#                 if address.version == 6 and address.prefixlen not in (127, 128):
#                     raise ValidationError(msg)
#             if address.ip == address.broadcast:
#                 msg = f"{address} is a broadcast address, which may not be assigned to an interface."
#                 raise ValidationError(msg)

#     def save(self, *args, **kwargs):
#         ipaddress = super().save(*args, **kwargs)

#         # Assign/clear this IPAddress as the primary for the associated Device/VirtualMachine.
#         interface = self.instance.assigned_object
#         if type(interface) in (Interface, VMInterface):
#             parent = interface.parent_object
#             if self.cleaned_data['primary_for_parent']:
#                 if ipaddress.address.version == 4:
#                     parent.primary_ip4 = ipaddress
#                 else:
#                     parent.primary_ip6 = ipaddress
#                 parent.save()
#             elif ipaddress.address.version == 4 and parent.primary_ip4 == ipaddress:
#                 parent.primary_ip4 = None
#                 parent.save()
#             elif ipaddress.address.version == 6 and parent.primary_ip6 == ipaddress:
#                 parent.primary_ip6 = None
#                 parent.save()

#         return ipaddress


# class IPAddressBulkAddForm(TenancyForm, NetBoxModelForm):
#     vrf = DynamicModelChoiceField(
#         queryset=VRF.objects.all(),
#         required=False,
#         label=_('VRF')
#     )

#     class Meta:
#         model = IPAddress
#         fields = [
#             'address', 'vrf', 'status', 'role', 'dns_name', 'description', 'tenant_group', 'tenant', 'tags',
#         ]


# class IPAddressAssignForm(BootstrapMixin, forms.Form):
#     vrf_id = DynamicModelChoiceField(
#         queryset=VRF.objects.all(),
#         required=False,
#         label=_('VRF')
#     )
#     q = forms.CharField(
#         required=False,
#         label=_('Search'),
#     )


# class FHRPGroupForm(NetBoxModelForm):

#     # Optionally create a new IPAddress along with the FHRPGroup
#     ip_vrf = DynamicModelChoiceField(
#         queryset=VRF.objects.all(),
#         required=False,
#         label=_('VRF')
#     )
#     ip_address = IPNetworkFormField(
#         required=False,
#         label=_('Address')
#     )
#     ip_status = forms.ChoiceField(
#         choices=add_blank_choice(IPAddressStatusChoices),
#         required=False,
#         label=_('Status')
#     )
#     comments = CommentField()

#     fieldsets = (
#         ('FHRP Group', ('protocol', 'group_id', 'name', 'description', 'tags')),
#         ('Authentication', ('auth_type', 'auth_key')),
#         ('Virtual IP Address', ('ip_vrf', 'ip_address', 'ip_status'))
#     )

#     class Meta:
#         model = FHRPGroup
#         fields = (
#             'protocol', 'group_id', 'auth_type', 'auth_key', 'name', 'ip_vrf', 'ip_address', 'ip_status', 'description',
#             'comments', 'tags',
#         )

#     def save(self, *args, **kwargs):
#         instance = super().save(*args, **kwargs)
#         user = getattr(instance, '_user', None)  # Set under FHRPGroupEditView.alter_object()

#         # Check if we need to create a new IPAddress for the group
#         if self.cleaned_data.get('ip_address'):
#             ipaddress = IPAddress(
#                 vrf=self.cleaned_data['ip_vrf'],
#                 address=self.cleaned_data['ip_address'],
#                 status=self.cleaned_data['ip_status'],
#                 role=FHRP_PROTOCOL_ROLE_MAPPINGS.get(self.cleaned_data['protocol'], IPAddressRoleChoices.ROLE_VIP),
#                 assigned_object=instance
#             )
#             ipaddress.populate_custom_field_defaults()
#             ipaddress.save()

#             # Check that the new IPAddress conforms with any assigned object-level permissions
#             if not IPAddress.objects.restrict(user, 'add').filter(pk=ipaddress.pk).first():
#                 raise PermissionsViolation()

#         return instance

#     def clean(self):
#         super().clean()

#         ip_vrf = self.cleaned_data.get('ip_vrf')
#         ip_address = self.cleaned_data.get('ip_address')
#         ip_status = self.cleaned_data.get('ip_status')

#         if ip_address:
#             ip_form = IPAddressForm({
#                 'address': ip_address,
#                 'vrf': ip_vrf,
#                 'status': ip_status,
#             })
#             if not ip_form.is_valid():
#                 self.errors.update({
#                     f'ip_{field}': error for field, error in ip_form.errors.items()
#                 })


# class FHRPGroupAssignmentForm(BootstrapMixin, forms.ModelForm):
#     group = DynamicModelChoiceField(
#         queryset=FHRPGroup.objects.all()
#     )

#     class Meta:
#         model = FHRPGroupAssignment
#         fields = ('group', 'priority')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         ipaddresses = self.instance.interface.ip_addresses.all()
#         for ipaddress in ipaddresses:
#             self.fields['group'].widget.add_query_param('related_ip', ipaddress.pk)




# class ServiceTemplateForm(NetBoxModelForm):
#     ports = NumericArrayField(
#         base_field=forms.IntegerField(
#             min_value=SERVICE_PORT_MIN,
#             max_value=SERVICE_PORT_MAX
#         ),
#         help_text=_("Comma-separated list of one or more port numbers. A range may be specified using a hyphen.")
#     )
#     comments = CommentField()

#     fieldsets = (
#         ('Service Template', (
#             'name', 'protocol', 'ports', 'description', 'tags',
#         )),
#     )

#     class Meta:
#         model = ServiceTemplate
#         fields = ('name', 'protocol', 'ports', 'description', 'comments', 'tags')


# class ServiceForm(NetBoxModelForm):
#     device = DynamicModelChoiceField(
#         queryset=Device.objects.all(),
#         required=False,
#         selector=True
#     )
#     virtual_machine = DynamicModelChoiceField(
#         queryset=VirtualMachine.objects.all(),
#         required=False,
#         selector=True
#     )
#     ports = NumericArrayField(
#         base_field=forms.IntegerField(
#             min_value=SERVICE_PORT_MIN,
#             max_value=SERVICE_PORT_MAX
#         ),
#         help_text=_("Comma-separated list of one or more port numbers. A range may be specified using a hyphen.")
#     )
#     ipaddresses = DynamicModelMultipleChoiceField(
#         queryset=IPAddress.objects.all(),
#         required=False,
#         label=_('IP Addresses'),
#         query_params={
#             'device_id': '$device',
#             'virtual_machine_id': '$virtual_machine',
#         }
#     )
#     comments = CommentField()

#     class Meta:
#         model = Service
#         fields = [
#             'device', 'virtual_machine', 'name', 'protocol', 'ports', 'ipaddresses', 'description', 'comments', 'tags',
#         ]


# class ServiceCreateForm(ServiceForm):
#     service_template = DynamicModelChoiceField(
#         queryset=ServiceTemplate.objects.all(),
#         required=False
#     )

#     class Meta(ServiceForm.Meta):
#         fields = [
#             'device', 'virtual_machine', 'service_template', 'name', 'protocol', 'ports', 'ipaddresses', 'description',
#             'tags',
#         ]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Fields which may be populated from a ServiceTemplate are not required
#         for field in ('name', 'protocol', 'ports'):
#             self.fields[field].required = False
#             del self.fields[field].widget.attrs['required']

#     def clean(self):
#         super().clean()
#         if self.cleaned_data['service_template']:
#             # Create a new Service from the specified template
#             service_template = self.cleaned_data['service_template']
#             self.cleaned_data['name'] = service_template.name
#             self.cleaned_data['protocol'] = service_template.protocol
#             self.cleaned_data['ports'] = service_template.ports
#             if not self.cleaned_data['description']:
#                 self.cleaned_data['description'] = service_template.description
#         elif not all(self.cleaned_data[f] for f in ('name', 'protocol', 'ports')):
#             raise forms.ValidationError("Must specify name, protocol, and port(s) if not using a service template.")


# #
# # L2VPN
# #


# class L2VPNForm(TenancyForm, NetBoxModelForm):
#     slug = SlugField()
#     import_targets = DynamicModelMultipleChoiceField(
#         queryset=RouteTarget.objects.all(),
#         required=False
#     )
#     export_targets = DynamicModelMultipleChoiceField(
#         queryset=RouteTarget.objects.all(),
#         required=False
#     )
#     comments = CommentField()

#     fieldsets = (
#         ('L2VPN', ('name', 'slug', 'type', 'identifier', 'description', 'tags')),
#         ('Route Targets', ('import_targets', 'export_targets')),
#         ('Tenancy', ('tenant_group', 'tenant')),
#     )

#     class Meta:
#         model = L2VPN
#         fields = (
#             'name', 'slug', 'type', 'identifier', 'import_targets', 'export_targets', 'tenant', 'description',
#             'comments', 'tags'
#         )


# class L2VPNTerminationForm(NetBoxModelForm):
#     l2vpn = DynamicModelChoiceField(
#         queryset=L2VPN.objects.all(),
#         required=True,
#         query_params={},
#         label=_('L2VPN'),
#         fetch_trigger='open'
#     )
#     vlan = DynamicModelChoiceField(
#         queryset=VLAN.objects.all(),
#         required=False,
#         selector=True,
#         label=_('VLAN')
#     )
#     interface = DynamicModelChoiceField(
#         queryset=Interface.objects.all(),
#         required=False,
#         selector=True
#     )
#     vminterface = DynamicModelChoiceField(
#         queryset=VMInterface.objects.all(),
#         required=False,
#         selector=True,
#         label=_('Interface')
#     )

#     class Meta:
#         model = L2VPNTermination
#         fields = ('l2vpn', )

#     def __init__(self, *args, **kwargs):
#         instance = kwargs.get('instance')
#         initial = kwargs.get('initial', {}).copy()

#         if instance:
#             if type(instance.assigned_object) is Interface:
#                 initial['interface'] = instance.assigned_object
#             elif type(instance.assigned_object) is VLAN:
#                 initial['vlan'] = instance.assigned_object
#             elif type(instance.assigned_object) is VMInterface:
#                 initial['vminterface'] = instance.assigned_object
#             kwargs['initial'] = initial

#         super().__init__(*args, **kwargs)

#     def clean(self):
#         super().clean()

#         interface = self.cleaned_data.get('interface')
#         vminterface = self.cleaned_data.get('vminterface')
#         vlan = self.cleaned_data.get('vlan')

#         if not (interface or vminterface or vlan):
#             raise ValidationError('A termination must specify an interface or VLAN.')
#         if len([x for x in (interface, vminterface, vlan) if x]) > 1:
#             raise ValidationError('A termination can only have one terminating object (an interface or VLAN).')

#         self.instance.assigned_object = interface or vminterface or vlan
