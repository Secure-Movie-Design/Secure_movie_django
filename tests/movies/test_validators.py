import pytest
from movies.validators import *


def test_number_validator():
    numberValidator = NumberValidator()
    with pytest.raises(ValidationError):
        numberValidator.validate("rewrewCIaoroewewr")


def test_uppercase_validator():
    uppercaseValidator = UppercaseValidator()
    with pytest.raises(ValidationError):
        uppercaseValidator.validate("passwordlowercase")


def test_lowercase_validator():
    lowercaseValidator = LowercaseValidator()
    with pytest.raises(ValidationError):
        lowercaseValidator.validate("PASSWORDUPPERCASE")


def test_symbol_validator():
    symbolValidator = SymbolValidator()
    with pytest.raises(ValidationError):
        symbolValidator.validate("Passwordwithoutsimbol43434")


def test_max_length_validator():
    maxLenghtValidator = MaximumLengthValidator(max_length=20)
    with pytest.raises(ValidationError):
        maxLenghtValidator.validate("P" * 21)
