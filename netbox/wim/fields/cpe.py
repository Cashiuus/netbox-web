from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from rest_framework import serializers



class CPEFormField(forms.Field):
    def to_python(self, value):
        if not value:
            return None


# Example CPE: cpe:/a:nginx:nginx:10.0.9
# TODO: Reference RHEL project for this: https://github.com/product-definition-center/product-definition-center/blob/af79f73c30fa5f5709ba03d584b7a49b83166b81/pdc/apps/release/serializers.py#L7

class CPEField(serializers.CharField):
    description = "A field for Common Platform Enumeration (CPE) product strings for automation use cases."

