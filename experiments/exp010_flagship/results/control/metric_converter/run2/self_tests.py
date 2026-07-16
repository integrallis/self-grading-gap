# test_solution.py

import pytest
from solution import convert

# US-1: Distance
def test_kilometers_to_miles():
    assert convert(1, 'kilometers', 'miles') == 0.621371  # 1 km * 0.621371
    assert convert(100, 'kilometers', 'miles') == 62.1371  # 100 km * 0.621371
    assert convert(0, 'kilometers', 'miles') == 0  # 0 km * 0.621371

# US-2: Temperature
def test_celsius_to_fahrenheit():
    assert convert(30, 'Celsius', 'Fahrenheit') == 86  # (30 * 9/5) + 32
    assert convert(0, 'Celsius', 'Fahrenheit') == 32  # (0 * 9/5) + 32
    assert convert(100, 'Celsius', 'Fahrenheit') == 212  # (100 * 9/5) + 32
    assert convert(-40, 'Celsius', 'Fahrenheit') == -40  # (-40 * 9/5) + 32

# US-3: Mass
def test_kilograms_to_pounds():
    assert convert(1, 'kilograms', 'pounds') == 2.2046226218487757  # 1 / 0.45359237
    assert convert(5, 'kilograms', 'pounds') == 11.023113109999999  # 5 / 0.45359237

# US-4: Volume
def test_liters_to_gallons():
    assert convert(3.785411784, 'liters', 'US gallons') == 1  # 3.785411784 liters is exactly 1 US gallon
    assert convert(4.54609, 'liters', 'UK gallons') == 1  # 4.54609 liters is exactly 1 UK gallon
    assert convert(1, 'liters', 'US gallons') < convert(1, 'liters', 'UK gallons')  # 1 liter < UK gallon

# US-5: Guarding the supported set
def test_unsupported_conversion():
    with pytest.raises(ValueError, match="unsupported conversion from kilometers to pounds"):
        convert(1, 'kilometers', 'pounds')
    with pytest.raises(ValueError, match="unsupported conversion from miles to kilometers"):
        convert(1, 'miles', 'kilometers')
    with pytest.raises(ValueError, match="unsupported conversion from Celsius to kilograms"):
        convert(1, 'Celsius', 'kilograms')
    with pytest.raises(ValueError, match="unsupported conversion from liters to liters"):
        convert(1, 'liters', 'liters')