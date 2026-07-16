# test_solution.py

import pytest
from solution import convert_units

# US-1: Distance
def test_kilometers_to_miles():
    assert convert_units(1, 'kilometers', 'miles') == 0.621371  # 1 km = 0.621371 miles
    assert convert_units(100, 'kilometers', 'miles') == 62.1371  # 100 km = 62.1371 miles
    assert convert_units(0, 'kilometers', 'miles') == 0.0  # 0 km = 0 miles

# US-2: Temperature
def test_celsius_to_fahrenheit():
    assert convert_units(30, 'Celsius', 'Fahrenheit') == 86.0  # (30 * 9/5) + 32 = 86
    assert convert_units(0, 'Celsius', 'Fahrenheit') == 32.0  # (0 * 9/5) + 32 = 32
    assert convert_units(100, 'Celsius', 'Fahrenheit') == 212.0  # (100 * 9/5) + 32 = 212
    assert convert_units(-40, 'Celsius', 'Fahrenheit') == -40.0  # (-40 * 9/5) + 32 = -40

# US-3: Mass
def test_kilograms_to_pounds():
    assert convert_units(1, 'kilograms', 'pounds') == 2.2046226218487757  # 1 kg = 1/0.45359237 pounds
    assert convert_units(5, 'kilograms', 'pounds') == 11.023113102172222  # 5 kg = 5/0.45359237 pounds

# US-4: Volume
def test_liters_to_us_gallons():
    assert convert_units(3.785411784, 'liters', 'US gallons') == 1.0  # 3.785411784 liters = 1 US gallon

def test_liters_to_uk_gallons():
    assert convert_units(4.54609, 'liters', 'UK gallons') == 1.0  # 4.54609 liters = 1 UK gallon

def test_liters_to_different_gallons():
    assert convert_units(4.54609, 'liters', 'US gallons') < convert_units(4.54609, 'liters', 'UK gallons')  # UK gallons < US gallons

# US-5: Guarding the supported set
def test_unsupported_conversion_reverse():
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'miles', 'kilometers')
    assert "unsupported conversion" in str(excinfo.value)
    assert "miles" in str(excinfo.value)
    assert "kilometers" in str(excinfo.value)

def test_unsupported_conversion_different_dimensions():
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'kilometers', 'pounds')
    assert "unsupported conversion" in str(excinfo.value)
    assert "kilometers" in str(excinfo.value)
    assert "pounds" in str(excinfo.value)

def test_unsupported_conversion_to_self():
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'liters', 'liters')
    assert "unsupported conversion" in str(excinfo.value)
    assert "liters" in str(excinfo.value)
    assert "liters" in str(excinfo.value)

def test_unsupported_conversion_unrecognized_unit():
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'meters', 'feet')
    assert "unsupported conversion" in str(excinfo.value)
    assert "meters" in str(excinfo.value)
    assert "feet" in str(excinfo.value)