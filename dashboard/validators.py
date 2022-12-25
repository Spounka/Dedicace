import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

empty_regex = r"^\s+$"
alphabetic_regex = r"^[A-z\-]([\s]{0,1}[A-z\-])[A-z]+$"
empty_validator = RegexValidator(regex=empty_regex, message=_("Value cannot be empty"), code=300, inverse_match=True)
alphabetic_validator = RegexValidator(regex=alphabetic_regex, message=_("Can only be alphabetic values"), code=300)


def validate_phone_number(phone_number):
    phone_re = r"(^(\+213)([1-9]{9})$)|^((05|06|07)[0-9]{8})$"
    if not re.match(phone_re, phone_number):
        raise ValidationError(_("Phone number must be either +213xxxxxxxxx or 0xxxxxxxxx"), code="20")
