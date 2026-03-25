import pytest


@pytest.fixture
def freezing_point():
    """Returns the freezing point of water in Celsius."""
    return 0.0


@pytest.fixture
def boiling_point():
    """Returns the boiling point of water in Celsius."""
    return 100.0


@pytest.fixture
def absolute_zero_c():
    """Returns absolute zero in Celsius."""
    return -273.15


@pytest.fixture
def absolute_zero_k():
    """Returns absolute zero in Kelvin."""
    return 0.0


@pytest.fixture
def body_temp():
    """Returns normal human body temperature in Celsius."""
    return 37.0


@pytest.fixture
def sample_conversions():
    """A list of (value, from_unit, to_unit, expected) tuples for parametrize-style use."""
    return [
        (0,      "C", "F", 32.0),
        (100,    "C", "F", 212.0),
        (32,     "F", "C", 0.0),
        (212,    "F", "C", 100.0),
        (0,      "C", "K", 273.15),
        (273.15, "K", "C", 0.0),
        (0,      "K", "C", -273.15),
    ]
