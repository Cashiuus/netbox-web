from netaddr import IPNetwork, IPSet
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

from dcim.models import Device, Site
from ipam.models import IPAddress

from wim.choices import *
from wim.models import *



class TestFQDN(TestCase):
    fqdns = FQDN.objects.bulk_create((
        FQDN(name='www.cnn.com'),
        FQDN(name='mail.google.com'),
        FQDN(name='www.wikipedia.org'),
    ))


    # Test Unique Enforcement

    @override_settings(ENFORCE_GLOBAL_UNIQUE=False)
    def test_duplicate_global(self):
        FQDN.objects.create(name='www.cnn.com'),
        dupe_record = FQDN(name='www.cnn.com')
        self.assertIsNone(dupe_record.clean())
    
    @override_settings(ENFORCE_GLOBAL_UNIQUE=True)
    def test_duplicate_global_unique(self):
        FQDN.objects.create(name='www.cnn.com'),
        dupe_record = FQDN(name='www.cnn.com')
        self.assertRaises(ValidationError, dupe_record.clean)
