import pytest
from solution import convert

# US-1: Distance
def test_kilometers_to_miles():
    # 1 km * 0.621371 = 0.621371 miles
    assert convert(1, 'kilometers', 'miles') == pytest.approx(0.621371)

def test_hundred_kilometers_to_miles():
    # 100 km * 0.621371 = 62.1371 miles
    assert convert(100, 'kilometers', 'miles') == pytest.approx(62.1371)

def test_zero_kilometers_to_miles():
    # 0 km * 0.621371 = 0 miles
    assert convert(0, 'kilometers', 'miles') == 0

# US-2: Temperature
def test_celsius_to_fahrenheit():
    # (30 * 9/5) + 32 = 86 degrees Fahrenheit
    assert convert(30, 'Celsius', 'Fahrenheit') == 86

def test_freezing_point_celsius_to_fahrenheit():
    # (0 * 9/5) + 32 = 32 degrees Fahrenheit
    assert convert(0, 'Celsius', 'Fahrenheit') == 32

def test_boiling_point_celsius_to_fahrenheit():
    # (100 * 9/5) + 32 = 212 degrees Fahrenheit
    assert convert(100, 'Celsius', 'Fahrenheit') == 212

def test_minus_40_celsius_to_fahrenheit():
    # (-40 * 9/5) + 32 = -40 degrees Fahrenheit
    assert convert(-40, 'Celsius', 'Fahrenheit') == -40

# US-3: Mass
def test_kilograms_to_pounds():
    # 1 kg / 0.45359237 = ~2.2046226218487757 pounds
    assert convert(1, 'kilograms', 'pounds') == pytest.approx(2.2046226218487757)

def test_five_kilograms_to_pounds():
    # 5 kg / 0.45359237 = ~11.023113109243878 pounds
    assert convert(5, 'kilograms', 'pounds') == pytest.approx(5 / 0.45359237)

# US-4: Volume
def test_liters_to_us_gallons():
    # 3.785411784 liters = 1 US gallon
    assert convert(3.785411784, 'liters', 'US gallons') == 1

def test_liters_to_uk_gallons():
    # 4.54609 liters = 1 UK gallon
    assert convert(4.54609, 'liters', 'UK gallons') == 1

def test_liters_to_us_vs_uk_gallons():
    # 1 liter to US gallons = ~0.264172 gallons
    # 1 liter to UK gallons = ~0.219969 gallons
    assert convert(1, 'liters', 'US gallons') > convert(1, 'liters', 'UK gallons')

def test_liters_to_us_gallons_intermediate():
    # 1 liter to US gallons = 1 / 3.785411784
    assert convert(1, 'liters', 'US gallons') == pytest.approx(1 / 3.785411784)

def test_liters_to_uk_gallons_intermediate():
    # 1 liter to UK gallons = 1 / 4.54609
    assert convert(1, 'liters', 'UK gallons') == pytest.approx(1 / 4.54609)

# US-5: Guarding the supported set
def test_unsupported_conversion_reverse():
    with pytest.raises(ValueError) as excinfo:
        convert(1, 'miles', 'kilometers')
    assert str(excinfo.value) == "unsupported conversion from miles to kilometers"

def test_unsupported_conversion_reverse_temperature():
    with pytest.raises(ValueError) as excinfo:
        convert(1, 'Fahrenheit', 'Celsius')
    assert str(excinfo.value) == "unsupported conversion from fahrenheit to celsius"

def test_unsupported_conversion_different_dimensions():
    with pytest.raises(ValueError) as excinfo:
        convert(1, 'kilometers', 'pounds')
    assert str(excinfo.value) == "unsupported conversion from kilometers to pounds"

def test_unsupported_conversion_to_itself():
    with pytest.raises(ValueError) as excinfo:
        convert(1, 'kilometers', 'kilometers')
    assert str(excinfo.value) == "unsupported conversion from kilometers to kilometers"

def test_unsupported_conversion_unrecognized_units():
    with pytest.raises(ValueError) as excinfo:
        convert(1, 'apples', 'oranges')
    assert str(excinfo.value) == "unsupported conversion from apples to oranges"

def test_unsupported_conversion_message_format():
    with pytest.raises(ValueError) as excinfo:
        convert(1, 'Celsius', 'pounds')
    assert str(excinfo.value) == "unsupported conversion from celsius to pounds"