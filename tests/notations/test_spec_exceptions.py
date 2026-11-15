import pytest
from sldb.notations.exceptions import NotationError, ParseError, ValidationError


def test_exception_hierarchy():
    assert issubclass(ParseError, NotationError)
    assert issubclass(ValidationError, NotationError)


def test_exceptions_are_catchable_as_base():
    with pytest.raises(NotationError):
        raise ParseError("bad yaml")
