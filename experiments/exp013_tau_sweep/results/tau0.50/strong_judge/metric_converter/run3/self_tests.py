import pytest
from solution import convert

# US-1: Distance
def test_kilometers_to_miles():
    assert convert(1, 'kilometers', 'miles') == 0.621371  # 1 km = 0.621371 miles
    assert convert(100, 'kilometers', 'miles') == 62.1371  # 100 km = 100 * 0.621371 miles
    assert convert(0, 'kilometers', 'miles') == 0.0  # 0 km = 0 miles

# US-2: Temperature
def test_celsius_to_fahrenheit():
    assert convert(30, 'Celsius', 'Fahrenheit') == 86.0  # (30 * 9/5) + 32 = 86
    assert convert(0, 'Celsius', 'Fahrenheit') == 32.0  # (0 * 9/5) + 32 = 32
    assert convert(100, 'Celsius', 'Fahrenheit') == 212.0  # (100 * 9/5) + 32 = 212
    assert convert(-40, 'Celsius', 'Fahrenheit') == -40.0  # (-40 * 9/5) + 32 = -40

# US-3: Mass
def test_kilograms_to_pounds():
    assert convert(1, 'kilograms', 'pounds') == 2.2046226218487757  # 1 kg = 1/0.45359237 pounds
    assert convert(5, 'kilograms', 'pounds') == pytest.approx(5 / 0.45359237)  # 5 kg = 5/0.45359237 pounds

# US-4: Volume
def test_liters_to_us_gallons():
    assert convert(3.785411784, 'liters', 'US gallons') == 1.0  # 3.785411784 liters = 1 US gallon

def test_liters_to_uk_gallons():
    assert convert(4.54609, 'liters', 'UK gallons') == 1.0  # 4.54609 liters = 1 UK gallon

def test_liters_to_us_vs_uk_gallons():
    assert convert(1, 'liters', 'US gallons') > convert(1, 'liters', 'UK gallons')  # 1 liter > UK gallons

# US-5: Guarding the supported set
def test_unsupported_conversion_units():
    with pytest.raises(ValueError) as excinfo:
        convert(1, 'miles', 'kilometers')
    assert "unsupported conversion" in str(excinfo.value)  # Check for error message
    assert "miles" in str(excinfo.value)  # Check for first unit
    assert "kilometers" in str(excinfo.value)  # Check for second unit

    with pytest.raises(ValueError) as excinfo:
        convert(1, 'Fahrenheit', 'Celsius')
    assert "unsupported conversion" in str(excinfo.value)  # Check for error message
    assert "fahrenheit" in str(excinfo.value)  # Check for first unit
    assert "celsius" in str(excinfo.value)  # Check for second unit

    with pytest.raises(ValueError) as excinfo:
        convert(1, 'kilograms', 'kilograms')
    assert "unsupported conversion" in str(excinfo.value)  # Check for error message
    assert "kilograms" in str(excinfo.value)  # Check for first unit
    assert "kilograms" in str(excinfo.value)  # Check for second unit

    with pytest.raises(ValueError) as excinfo:
        convert(1, 'liters', 'kilometers')
    assert "unsupported conversion" in str(excinfo.value)  # Check for error message
    assert "liters" in str(excinfo.value)  # Check for first unit
    assert "kilometers" in str(excinfo.value)  # Check for second unit

    # Test for unsupported unit
    with pytest.raises(ValueError) as excinfo:
        convert(1, 'meters', 'miles')
    assert "unsupported conversion" in str(excinfo.value)  # Check for error message
    assert "meters" in str(excinfo.value)  # Check for first unit
    assert "miles" in str(excinfo.value)  # Check for second unit