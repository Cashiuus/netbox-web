# File Purpose: I think this file is intended for robust pre-defined querysets
#               that are also restricted based on user permissions, and are linked
#               to the managers.py file for use.


from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.models.expressions import RawSQL

from utilities.querysets import RestrictedQuerySet



# -- Pre-Defined Querysets Important for administration --
pass
