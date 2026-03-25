import pytest
from src.converter import (
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    celsius_to_kelvin,
    kelvin_to_celsius,
    convert,
    ABSOLUTE_ZERO_C,
)


# ---------------------------------------------------------------------------
# celsius_to_fahrenheit
# ---------------------------------------------------------------------------

class TestCelsiusToFahrenheit:

    def test_freezing_point(self, freezing_point):
        assert celsius_to_fahrenheit(freezing_point) == 32.0

    def test_boiling_point(self, boiling_point):
        assert celsius_to_fahrenheit(boiling_point) == 212.0

    def test_body_temp(self, body_temp):
        assert celsius_to_fahrenheit(body_temp) == pytest.approx(98.6, rel=1e-3)

    @pytest.mark.parametrize("c, expected_f", [
        (-40,   -40.0),   # where the two scales meet
        (20,     68.0),
        (-10,    14.0),
    ])
    def test_parametrized(self, c, expected_f):
        assert celsius_to_fahrenheit(c) == pytest.approx(expected_f, rel=1e-6)

    @pytest.mark.edge
    def test_absolute_zero(self, absolute_zero_c):
        assert celsius_to_fahrenheit(absolute_zero_c) == pytest.approx(-459.67, rel=1e-4)

    @pytest.mark.edge
    def test_below_absolute_zero_raises(self):
        with pytest.raises(ValueError):
            celsius_to_fahrenheit(ABSOLUTE_ZERO_C - 0.01)


# ---------------------------------------------------------------------------
# fahrenheit_to_celsius
# ---------------------------------------------------------------------------

class TestFahrenheitToCelsius:

    def test_freezing_point(self):
        assert fahrenheit_to_celsius(32) == pytest.approx(0.0)

    def test_boiling_point(self):
        assert fahrenheit_to_celsius(212) == pytest.approx(100.0)

    @pytest.mark.parametrize("f, expected_c", [
        (-40,  -40.0),
        (68,    20.0),
        (98.6,  37.0),
    ])
    def test_parametrized(self, f, expected_c):
        assert fahrenheit_to_celsius(f) == pytest.approx(expected_c, rel=1e-3)

    @pytest.mark.edge
    def test_negative_fahrenheit(self):
        result = fahrenheit_to_celsius(-459.67)
        assert result == pytest.approx(ABSOLUTE_ZERO_C, rel=1e-3)


# ---------------------------------------------------------------------------
# celsius_to_kelvin
# ---------------------------------------------------------------------------

class TestCelsiusToKelvin:

    def test_freezing_point(self, freezing_point):
        assert celsius_to_kelvin(freezing_point) == pytest.approx(273.15)

    def test_boiling_point(self, boiling_point):
        assert celsius_to_kelvin(boiling_point) == pytest.approx(373.15)

    @pytest.mark.edge
    def test_absolute_zero_gives_zero_kelvin(self, absolute_zero_c):
        assert celsius_to_kelvin(absolute_zero_c) == pytest.approx(0.0, abs=1e-9)

    @pytest.mark.edge
    def test_below_absolute_zero_raises(self):
        with pytest.raises(ValueError):
            celsius_to_kelvin(ABSOLUTE_ZERO_C - 1)

    @pytest.mark.parametrize("c, expected_k", [
        (0,    273.15),
        (100,  373.15),
        (25,   298.15),
    ])
    def test_parametrized(self, c, expected_k):
        assert celsius_to_kelvin(c) == pytest.approx(expected_k)


# ---------------------------------------------------------------------------
# kelvin_to_celsius
# ---------------------------------------------------------------------------

class TestKelvinToCelsius:

    def test_freezing_point(self):
        assert kelvin_to_celsius(273.15) == pytest.approx(0.0, abs=1e-9)

    def test_boiling_point(self):
        assert kelvin_to_celsius(373.15) == pytest.approx(100.0)

    @pytest.mark.edge
    def test_zero_kelvin(self, absolute_zero_k):
        assert kelvin_to_celsius(absolute_zero_k) == pytest.approx(ABSOLUTE_ZERO_C)

    @pytest.mark.edge
    def test_negative_kelvin_raises(self):
        with pytest.raises(ValueError):
            kelvin_to_celsius(-1)

    @pytest.mark.parametrize("k, expected_c", [
        (273.15, 0.0),
        (373.15, 100.0),
        (0,      -273.15),
    ])
    def test_parametrized(self, k, expected_c):
        assert kelvin_to_celsius(k) == pytest.approx(expected_c)


# ---------------------------------------------------------------------------
# convert() dispatcher
# ---------------------------------------------------------------------------

class TestConvert:

    @pytest.mark.parametrize("value, from_unit, to_unit, expected", [
        (100,    "C", "F", 212.0),
        (32,     "F", "C", 0.0),
        (0,      "C", "K", 273.15),
        (273.15, "K", "C", 0.0),
        (32,     "F", "K", 273.15),
        (273.15, "K", "F", 32.0),
    ])
    def test_all_conversion_pairs(self, value, from_unit, to_unit, expected):
        assert convert(value, from_unit, to_unit) == pytest.approx(expected, rel=1e-4)

    def test_same_unit_returns_value(self, boiling_point):
        assert convert(boiling_point, "C", "C") == boiling_point

    def test_same_unit_kelvin(self):
        assert convert(300.0, "K", "K") == 300.0

    def test_case_insensitive_from(self):
        assert convert(100, "c", "F") == pytest.approx(212.0)

    def test_case_insensitive_to(self):
        assert convert(100, "C", "f") == pytest.approx(212.0)

    def test_case_insensitive_both(self):
        assert convert(0, "c", "k") == pytest.approx(273.15)

    @pytest.mark.edge
    def test_unknown_from_unit_raises(self):
        with pytest.raises(ValueError):
            convert(100, "X", "C")

    @pytest.mark.edge
    def test_unknown_to_unit_raises(self):
        with pytest.raises(ValueError):
            convert(100, "C", "Z")

    @pytest.mark.edge
    def test_below_absolute_zero_raises(self):
        with pytest.raises(ValueError):
            convert(ABSOLUTE_ZERO_C - 1, "C", "K")

    @pytest.mark.edge
    def test_negative_kelvin_input_raises(self):
        with pytest.raises(ValueError):
            convert(-5, "K", "C")

    def test_uses_fixture_sample_conversions(self, sample_conversions):
        for value, from_u, to_u, expected in sample_conversions:
            assert convert(value, from_u, to_u) == pytest.approx(expected, rel=1e-4)

    @pytest.mark.slow
    def test_round_trip_c_f_c(self, boiling_point):
        """Round-trip: C → F → C should return original value."""
        f = convert(boiling_point, "C", "F")
        back = convert(f, "F", "C")
        assert back == pytest.approx(boiling_point, rel=1e-9)

    @pytest.mark.slow
    def test_round_trip_c_k_c(self, body_temp):
        """Round-trip: C → K → C should return original value."""
        k = convert(body_temp, "C", "K")
        back = convert(k, "K", "C")
        assert back == pytest.approx(body_temp, rel=1e-9)
