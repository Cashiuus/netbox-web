from django import forms
from django.utils.translation import gettext as _

from utilities.forms import BootstrapMixin
from utilities.forms.fields import ExpandableIPAddressField

__all__ = (
    # 'IPAddressBulkCreateForm',
    # 'DomainBulkCreateForm',
    # 'FQDNBulkCreateForm',
)




class DomainBulkCreateForm(BootstrapMixin, forms.Form):
    pass
