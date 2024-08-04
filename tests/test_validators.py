"""
Test /gos/validators.py
"""

from gos.validators import exists


def test_exists_string_valid() -> bool:
    """When passed a string to exists, it should be True"""
    assert exists("test")


def test_exists_number_valid() -> bool:
    """When passed a int to exists, it should be True"""
    assert exists(123)


def test_exists_none_valid() -> bool:
    """When passed a None to exists, it should be False"""
    assert not exists(None)
