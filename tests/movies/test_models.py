import pytest
from mixer.backend.django import mixer


def test_mock(db):
    assert 5 + 4 == 9
