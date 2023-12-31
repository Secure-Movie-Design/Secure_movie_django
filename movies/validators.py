
from gettext import ngettext
import re
from django.contrib.auth import password_validation
from django.forms import ValidationError


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                self.get_help_text(),
                code='password_no_number',
            )

    @staticmethod
    def get_help_text():
        return (
            "Your password must contain at least 1 digit, 0-9."
        )


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                self.get_help_text(),
                code='password_no_upper',
            )

    @staticmethod
    def get_help_text():
        return (
            "Your password must contain at least 1 uppercase letter, A-Z."
        )


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                self.get_help_text(),
                code='password_no_lower',
            )

    @staticmethod
    def get_help_text():
        return (
            "Your password must contain at least 1 lowercase letter, a-z."
        )


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                self.get_help_text(),
                code='password_no_symbol',
            )

    @staticmethod
    def get_help_text():
        return (
            "Your password must contain at least 1 symbol: " +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )


class MaximumLengthValidator:
    """
    Validate that the password is of a maximum length.
    """

    def __init__(self, max_length=30):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                ngettext(
                    "This password is too long. It must contain at maximum "
                    "%(max_length)d characters.",
                    "This password is too long. It must contain at maximum "
                    "%(max_length)d characters.",
                    self.max_length,
                ),
                code="password_too_long",
                params={"max_length": self.max_length},
            )

    def get_help_text(self):
        return ngettext(
            "Your password must contain at maximum %(max_length)d characters.",
            "Your password must contain at maximum %(max_length)d characters.",
            self.max_length,
        ) % {"max_length": self.max_length}
