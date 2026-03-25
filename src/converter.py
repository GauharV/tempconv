# Absolute zero in Celsius
ABSOLUTE_ZERO_C = -273.15


def celsius_to_fahrenheit(c: float) -> float:
    """Convert Celsius to Fahrenheit.

    Formula: (c * 9/5) + 32
    Example: 0°C → 32.0°F, 100°C → 212.0°F
    """
    if c < ABSOLUTE_ZERO_C:
        raise ValueError(f"Temperature {c}°C is below absolute zero ({ABSOLUTE_ZERO_C}°C).")
    return (c * 9 / 5) + 32


def fahrenheit_to_celsius(f: float) -> float:
    """Convert Fahrenheit to Celsius.

    Formula: (f - 32) * 5/9
    Example: 32°F → 0.0°C, 212°F → 100.0°C
    """
    return (f - 32) * 5 / 9


def celsius_to_kelvin(c: float) -> float:
    """Convert Celsius to Kelvin.

    Formula: c + 273.15
    Raises: ValueError if c < ABSOLUTE_ZERO_C
    Example: 0°C → 273.15K, -273.15°C → 0.0K
    """
    if c < ABSOLUTE_ZERO_C:
        raise ValueError(f"Temperature {c}°C is below absolute zero ({ABSOLUTE_ZERO_C}°C).")
    return c - ABSOLUTE_ZERO_C


def kelvin_to_celsius(k: float) -> float:
    """Convert Kelvin to Celsius.

    Formula: k - 273.15
    Raises: ValueError if k < 0
    Example: 273.15K → 0.0°C, 0K → -273.15°C
    """
    if k < 0:
        raise ValueError(f"Kelvin cannot be negative. Got: {k}.")
    return k + ABSOLUTE_ZERO_C


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert a temperature between any supported units.

    Units: 'C' (Celsius), 'F' (Fahrenheit), 'K' (Kelvin)
    Raises: ValueError for unknown units or invalid temperatures.

    Examples:
        convert(100, 'C', 'F') → 212.0
        convert(32, 'F', 'C') → 0.0
        convert(0, 'C', 'K') → 273.15
    """
    # Normalize to uppercase so 'c' and 'C' both work
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()

    valid_units = {"C", "F", "K"}
    if from_unit not in valid_units:
        raise ValueError(f"Unknown unit: '{from_unit}'. Must be one of {valid_units}.")
    if to_unit not in valid_units:
        raise ValueError(f"Unknown unit: '{to_unit}'. Must be one of {valid_units}.")

    # If same unit, return as-is
    if from_unit == to_unit:
        return float(value)

    # Convert via Celsius as the intermediate unit
    if from_unit == "C":
        celsius = float(value)
    elif from_unit == "F":
        celsius = fahrenheit_to_celsius(value)
    else:  # K
        celsius = kelvin_to_celsius(value)

    if to_unit == "C":
        return celsius
    elif to_unit == "F":
        return celsius_to_fahrenheit(celsius)
    else:  # K
        return celsius_to_kelvin(celsius)
