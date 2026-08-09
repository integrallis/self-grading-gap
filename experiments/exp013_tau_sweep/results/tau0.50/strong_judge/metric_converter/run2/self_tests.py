# test_solution.py

import pytest
from solution import convert_units  # Assuming the function to be tested is named convert_units

# US-1: Distance
def test_kilometers_to_miles_conversion():
    assert convert_units(1, 'kilometers', 'miles') == 0.621371  # 1 km = 0.621371 miles
    assert convert_units(100, 'kilometers', 'miles') == 62.1371  # 100 km = 100 * 0.621371 miles
    assert convert_units(0, 'kilometers', 'miles') == 0  # 0 km = 0 miles

# US-2: Temperature
def test_celsius_to_fahrenheit_conversion():
    assert convert_units(30, 'Celsius', 'Fahrenheit') == 86  # (30 * 9/5) + 32 = 86
    assert convert_units(0, 'Celsius', 'Fahrenheit') == 32  # (0 * 9/5) + 32 = 32
    assert convert_units(100, 'Celsius', 'Fahrenheit') == 212  # (100 * 9/5) + 32 = 212
    assert convert_units(-40, 'Celsius', 'Fahrenheit') == -40  # (-40 * 9/5) + 32 = -40

# US-3: Mass
def test_kilograms_to_pounds_conversion():
    assert convert_units(1, 'kilograms', 'pounds') == 2.2046226218487757  # 1 kg = 1 / 0.45359237 pounds
    assert convert_units(5, 'kilograms', 'pounds') == pytest.approx(11.02311310)  # 5 kg = 5 / 0.45359237 pounds

# US-4: Volume
def test_liters_to_us_gallons_conversion():
    assert convert_units(3.785411784, 'liters', 'US gallons') == 1  # 3.785411784 liters = 1 US gallon

def test_liters_to_uk_gallons_conversion():
    assert convert_units(4.54609, 'liters', 'UK gallons') == 1  # 4.54609 liters = 1 UK gallon

def test_liters_to_gallons_different_standards():
    assert convert_units(4.54609, 'liters', 'US gallons') > convert_units(4.54609, 'liters', 'UK gallons')  # US gallons are more than UK gallons

# US-5: Guarding the supported set
def test_unsupported_conversion_reverse_direction():
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'miles', 'kilometers')
    assert isinstance(excinfo.value, ValueError) and type(excinfo.value) is not ValueError
    assert "unsupported conversion" in str(excinfo.value)
    assert "miles" in str(excinfo.value)
    assert "kilometers" in str(excinfo.value)

def test_unsupported_conversion_reverse_direction_temperature():
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'Fahrenheit', 'Celsius')
    assert isinstance(excinfo.value, ValueError) and type(excinfo.value) is not ValueError
    assert "unsupported conversion" in str(excinfo.value)
    assert "fahrenheit" in str(excinfo.value)
    assert "celsius" in str(excinfo.value)

def test_unsupported_conversion_different_dimensions():
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'kilometers', 'pounds')
    assert isinstance(excinfo.value, ValueError) and type(excinfo.value) is not ValueError
    assert "unsupported conversion" in str(excinfo.value)
    assert "kilometers" in str(excinfo.value)
    assert "pounds" in str(excinfo.value)

def test_unsupported_conversion_same_unit():
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'liters', 'liters')
    assert isinstance(excinfo.value, ValueError) and type(excinfo.value) is not ValueError
    assert "unsupported conversion" in str(excinfo.value)
    assert "liters" in str(excinfo.value)
    assert "liters" in str(excinfo.value)

def test_unsupported_conversion_unsupported_units():
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'meters', 'pounds')
    assert isinstance(excinfo.value, ValueError) and type(excinfo.value) is not ValueError
    assert "unsupported conversion" in str(excinfo.value)
    assert "meters" in str(excinfo.value)
    assert "pounds" in str(excinfo.value)

def test_unsupported_conversion_reverse_direction_volume_us():
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'US gallons', 'liters')
    assert isinstance(excinfo.value, ValueError) and type(excinfo.value) is not ValueError
    assert "unsupported conversion" in str(excinfo.value)
    assert "us gallons" in str(excinfo.value)
    assert "liters" in str(excinfo.value)

def test_unsupported_conversion_reverse_direction_volume_uk():
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'UK gallons', 'liters')
    assert isinstance(excinfo.value, ValueError) and type(excinfo.value) is not ValueError
    assert "unsupported conversion" in str(excinfo.value)
    assert "uk gallons" in str(excinfo.value)
    assert "liters" in str(excinfo.value)