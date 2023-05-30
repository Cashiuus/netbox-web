from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator, RegexValidator


DNSValidator = RegexValidator(
    regex=r'^([0-9A-Za-z_-]+|\*)(\.[0-9A-Za-z_-]+)*\.?$',
    message='Only alphanumeric characters, asterisks, hyphens, periods, and underscores are allowed in DNS names',
    code='invalid'
)



def validate_cpe(cpe_str):
    """ First-pass validator for a CPE string, can use improvements. 
    """
    if not cpe_str.startswith("cpe:"):
        return "CPE must start with 'cpe:'"
    else:
        return None


# CPEValidator = BaseValidator(
#     limit_value = 
# )