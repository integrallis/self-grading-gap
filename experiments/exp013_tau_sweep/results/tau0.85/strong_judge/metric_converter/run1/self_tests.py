import pytest
from solution import convert_units

# US-1: Distance
def test_kilometers_to_miles():
    assert convert_units(1, 'kilometers', 'miles') == 0.621371  # 1 km = 0.621371 miles
    assert convert_units(100, 'kilometers', 'miles') == 62.1371  # 100 km = 100 * 0.621371 miles
    assert convert_units(0, 'kilometers', 'miles') == 0  # 0 km = 0 miles

# US-2: Temperature
def test_celsius_to_fahrenheit():
    assert convert_units(30, 'celsius', 'fahrenheit') == 86  # (30 * 9/5) + 32 = 86
    assert convert_units(0, 'celsius', 'fahrenheit') == 32  # (0 * 9/5) + 32 = 32
    assert convert_units(100, 'celsius', 'fahrenheit') == 212  # (100 * 9/5) + 32 = 212
    assert convert_units(-40, 'celsius', 'fahrenheit') == -40  # (-40 * 9/5) + 32 = -40

# US-3: Mass
def test_kilograms_to_pounds():
    assert convert_units(1, 'kilograms', 'pounds') == 2.2046226218487757  # 1 kg = 1 / 0.45359237 pounds
    assert convert_units(5, 'kilograms', 'pounds') == pytest.approx(11.023113109243878)  # 5 kg = 5 / 0.45359237 pounds

# US-4: Volume
def test_liters_to_us_gallons():
    assert convert_units(3.785411784, 'liters', 'us_gallons') == 1  # 3.785411784 liters = 1 US gallon

def test_liters_to_uk_gallons():
    assert convert_units(4.54609, 'liters', 'uk_gallons') == 1  # 4.54609 liters = 1 UK gallon

def test_liters_comparison():
    us_gallons = convert_units(1, 'liters', 'us_gallons')
    uk_gallons = convert_units(1, 'liters', 'uk_gallons')
    assert us_gallons > uk_gallons  # 1 L yields more US gallons than UK gallons

# US-5: Guarding the supported set
def test_unsupported_conversion():
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'miles', 'kilometers')  # Reversed direction not supported
    assert "unsupported conversion" in str(excinfo.value)
    assert "miles" in str(excinfo.value)
    assert "kilometers" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'kilograms', 'liters')  # Different dimensions not supported
    assert "unsupported conversion" in str(excinfo.value)
    assert "kilograms" in str(excinfo.value)
    assert "liters" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'kilometers', 'kilometers')  # Same unit conversion not supported
    assert "unsupported conversion" in str(excinfo.value)
    assert "kilometers" in str(excinfo.value)
    assert "kilometers" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        convert_units(32, 'fahrenheit', 'celsius')  # Reverse direction not supported
    assert "unsupported conversion" in str(excinfo.value)
    assert "fahrenheit" in str(excinfo.value)
    assert "celsius" in str(excinfo.value)

    # Test for unsupported units
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'unknown_unit', 'miles')  # Unsupported unit
    assert "unsupported conversion" in str(excinfo.value)
    assert "unknown_unit" in str(excinfo.value)