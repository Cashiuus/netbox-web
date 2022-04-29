from circuits.models import Circuit, CircuitTermination, Provider
from dcim.models import *
from netbox.forms import NetBoxModelForm
from tenancy.forms import TenancyForm
from utilities.forms import DynamicModelChoiceField, DynamicModelMultipleChoiceField, StaticSelect

__all__ = (
    'ConnectCableToCircuitTerminationForm',
    'ConnectCableToConsolePortForm',
    'ConnectCableToConsoleServerPortForm',
    'ConnectCableToFrontPortForm',
    'ConnectCableToInterfaceForm',
    'ConnectCableToPowerFeedForm',
    'ConnectCableToPowerPortForm',
    'ConnectCableToPowerOutletForm',
    'ConnectCableToRearPortForm',
)


class ConnectCableToDeviceForm(TenancyForm, NetBoxModelForm):
    """
    Base form for connecting a Cable to a Device component
    """
    # Termination A
    termination_a_ids = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(),
        label='Name',
        disabled_indicator='_occupied'
    )

    # Termination B
    termination_b_region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        label='Region',
        required=False,
        initial_params={
            'sites': '$termination_b_site'
        }
    )
    termination_b_sitegroup = DynamicModelChoiceField(
        queryset=SiteGroup.objects.all(),
        label='Site group',
        required=False,
        initial_params={
            'sites': '$termination_b_site'
        }
    )
    termination_b_site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        label='Site',
        required=False,
        query_params={
            'region_id': '$termination_b_region',
            'group_id': '$termination_b_sitegroup',
        }
    )
    termination_b_location = DynamicModelChoiceField(
        queryset=Location.objects.all(),
        label='Location',
        required=False,
        null_option='None',
        query_params={
            'site_id': '$termination_b_site'
        }
    )
    termination_b_rack = DynamicModelChoiceField(
        queryset=Rack.objects.all(),
        label='Rack',
        required=False,
        null_option='None',
        query_params={
            'site_id': '$termination_b_site',
            'location_id': '$termination_b_location',
        }
    )
    termination_b_device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        label='Device',
        required=False,
        query_params={
            'site_id': '$termination_b_site',
            'location_id': '$termination_b_location',
            'rack_id': '$termination_b_rack',
        }
    )
    termination_b_ids = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(),
        label='Name',
        disabled_indicator='_occupied'
    )

    class Meta:
        model = Cable
        fields = [
            'termination_a_ids', 'termination_b_region', 'termination_b_sitegroup', 'termination_b_site',
            'termination_b_rack', 'termination_b_device', 'termination_b_ids', 'type', 'status', 'tenant_group',
            'tenant', 'label', 'color', 'length', 'length_unit', 'tags',
        ]
        widgets = {
            'status': StaticSelect,
            'type': StaticSelect,
            'length_unit': StaticSelect,
        }

    def clean_termination_a_ids(self):
        # Return the PK rather than the object
        return [getattr(obj, 'pk') for obj in self.cleaned_data['termination_a_ids']]

    def clean_termination_b_ids(self):
        # Return the PK rather than the object
        return [getattr(obj, 'pk') for obj in self.cleaned_data['termination_b_ids']]


class ConnectCableToConsolePortForm(ConnectCableToDeviceForm):
    termination_b_ids = DynamicModelMultipleChoiceField(
        queryset=ConsolePort.objects.all(),
        label='Name',
        disabled_indicator='_occupied',
        query_params={
            'device_id': '$termination_b_device'
        }
    )


class ConnectCableToConsoleServerPortForm(ConnectCableToDeviceForm):
    termination_b_ids = DynamicModelMultipleChoiceField(
        queryset=ConsoleServerPort.objects.all(),
        label='Name',
        disabled_indicator='_occupied',
        query_params={
            'device_id': '$termination_b_device'
        }
    )


class ConnectCableToPowerPortForm(ConnectCableToDeviceForm):
    termination_b_ids = DynamicModelMultipleChoiceField(
        queryset=PowerPort.objects.all(),
        label='Name',
        disabled_indicator='_occupied',
        query_params={
            'device_id': '$termination_b_device'
        }
    )


class ConnectCableToPowerOutletForm(ConnectCableToDeviceForm):
    termination_b_ids = DynamicModelMultipleChoiceField(
        queryset=PowerOutlet.objects.all(),
        label='Name',
        disabled_indicator='_occupied',
        query_params={
            'device_id': '$termination_b_device'
        }
    )


class ConnectCableToInterfaceForm(ConnectCableToDeviceForm):
    termination_b_ids = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(),
        label='Name',
        disabled_indicator='_occupied',
        query_params={
            'device_id': '$termination_b_device',
            'kind': 'physical',
        }
    )


class ConnectCableToFrontPortForm(ConnectCableToDeviceForm):
    termination_b_ids = DynamicModelMultipleChoiceField(
        queryset=FrontPort.objects.all(),
        label='Name',
        disabled_indicator='_occupied',
        query_params={
            'device_id': '$termination_b_device'
        }
    )


class ConnectCableToRearPortForm(ConnectCableToDeviceForm):
    termination_b_ids = DynamicModelMultipleChoiceField(
        queryset=RearPort.objects.all(),
        label='Name',
        disabled_indicator='_occupied',
        query_params={
            'device_id': '$termination_b_device'
        }
    )


class ConnectCableToCircuitTerminationForm(TenancyForm, NetBoxModelForm):
    # Termination A
    termination_a_ids = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(),
        label='Side',
        disabled_indicator='_occupied'
    )

    # Termination B
    termination_b_provider = DynamicModelChoiceField(
        queryset=Provider.objects.all(),
        label='Provider',
        required=False
    )
    termination_b_region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        label='Region',
        required=False,
        initial_params={
            'sites': '$termination_b_site'
        }
    )
    termination_b_sitegroup = DynamicModelChoiceField(
        queryset=SiteGroup.objects.all(),
        label='Site group',
        required=False,
        initial_params={
            'sites': '$termination_b_site'
        }
    )
    termination_b_site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        label='Site',
        required=False,
        query_params={
            'region_id': '$termination_b_region',
            'group_id': '$termination_b_sitegroup',
        }
    )
    termination_b_circuit = DynamicModelChoiceField(
        queryset=Circuit.objects.all(),
        label='Circuit',
        query_params={
            'provider_id': '$termination_b_provider',
            'site_id': '$termination_b_site',
        }
    )
    termination_b_ids = DynamicModelMultipleChoiceField(
        queryset=CircuitTermination.objects.all(),
        label='Side',
        disabled_indicator='_occupied',
        query_params={
            'circuit_id': '$termination_b_circuit'
        }
    )

    class Meta(ConnectCableToDeviceForm.Meta):
        fields = [
            'termination_a_ids', 'termination_b_provider', 'termination_b_region', 'termination_b_sitegroup',
            'termination_b_site', 'termination_b_circuit', 'termination_b_ids', 'type', 'status', 'tenant_group',
            'tenant', 'label', 'color', 'length', 'length_unit', 'tags',
        ]

    def clean_termination_a_id(self):
        # Return the PK rather than the object
        return getattr(self.cleaned_data['termination_a_id'], 'pk', None)

    def clean_termination_b_id(self):
        # Return the PK rather than the object
        return getattr(self.cleaned_data['termination_b_id'], 'pk', None)


class ConnectCableToPowerFeedForm(TenancyForm, NetBoxModelForm):
    # Termination A
    termination_a_ids = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(),
        label='Name',
        disabled_indicator='_occupied'
    )

    # Termination B
    termination_b_region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        label='Region',
        required=False,
        initial_params={
            'sites': '$termination_b_site'
        }
    )
    termination_b_sitegroup = DynamicModelChoiceField(
        queryset=SiteGroup.objects.all(),
        label='Site group',
        required=False,
        initial_params={
            'sites': '$termination_b_site'
        }
    )
    termination_b_site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        label='Site',
        required=False,
        query_params={
            'region_id': '$termination_b_region',
            'group_id': '$termination_b_sitegroup',
        }
    )
    termination_b_location = DynamicModelChoiceField(
        queryset=Location.objects.all(),
        label='Location',
        required=False,
        query_params={
            'site_id': '$termination_b_site'
        }
    )
    termination_b_powerpanel = DynamicModelChoiceField(
        queryset=PowerPanel.objects.all(),
        label='Power Panel',
        required=False,
        query_params={
            'site_id': '$termination_b_site',
            'location_id': '$termination_b_location',
        }
    )
    termination_b_ids = DynamicModelMultipleChoiceField(
        queryset=PowerFeed.objects.all(),
        label='Name',
        disabled_indicator='_occupied',
        query_params={
            'power_panel_id': '$termination_b_powerpanel'
        }
    )

    class Meta(ConnectCableToDeviceForm.Meta):
        fields = [
            'termination_a_ids', 'termination_b_region', 'termination_b_sitegroup', 'termination_b_site',
            'termination_b_location', 'termination_b_powerpanel', 'termination_b_ids', 'type', 'status', 'tenant_group',
            'tenant', 'label', 'color', 'length', 'length_unit', 'tags',
        ]

    def clean_termination_a_id(self):
        # Return the PK rather than the object
        return getattr(self.cleaned_data['termination_a_id'], 'pk', None)

    def clean_termination_b_id(self):
        # Return the PK rather than the object
        return getattr(self.cleaned_data['termination_b_id'], 'pk', None)
