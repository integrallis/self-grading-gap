from solution import convert_units
import pytest

def test_kilometers_to_miles():
    assert abs(convert_units(1, 'kilometers', 'miles') - 0.621371) < 1e-9  # 1 km = 0.621371 miles
    assert abs(convert_units(100, 'kilometers', 'miles') - 62.1371) < 1e-9  # 100 km = 62.1371 miles
    assert convert_units(0, 'kilometers', 'miles') == 0.0                   # 0 km = 0 miles

def test_celsius_to_fahrenheit():
    assert abs(convert_units(30, 'Celsius', 'Fahrenheit') - 86.0) < 1e-9   # 30 °C = 86 °F
    assert convert_units(0, 'Celsius', 'Fahrenheit') == 32.0                # 0 °C = 32 °F
    assert convert_units(100, 'Celsius', 'Fahrenheit') == 212.0             # 100 °C = 212 °F
    assert convert_units(-40, 'Celsius', 'Fahrenheit') == -40.0             # -40 °C = -40 °F

def test_kilograms_to_pounds():
    assert abs(convert_units(1, 'kilograms', 'pounds') - (1 / 0.45359237)) < 1e-9  # 1 kg = 1 / 0.45359237 pounds
    assert abs(convert_units(5, 'kilograms', 'pounds') - (5 / 0.45359237)) < 1e-9    # 5 kg = 5 / 0.45359237 pounds

def test_liters_to_us_gallons():
    assert abs(convert_units(3.785411784, 'liters', 'US gallons') - 1.0) < 1e-9  # 3.785411784 liters = 1 US gallon

def test_liters_to_uk_gallons():
    assert abs(convert_units(4.54609, 'liters', 'UK gallons') - 1.0) < 1e-9  # 4.54609 liters = 1 UK gallon

def test_liters_to_different_standards():
    assert convert_units(4.54609, 'liters', 'UK gallons') < convert_units(4.54609, 'liters', 'US gallons')  # UK gallons < US gallons

def test_unsupported_conversion_reverse():
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'miles', 'kilometers')
    assert "unsupported conversion" in str(excinfo.value) and "miles" in str(excinfo.value) and "kilometers" in str(excinfo.value)
    assert type(excinfo.value) is not ValueError

def test_unsupported_conversion_reverse_celsius_to_fahrenheit():
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'Fahrenheit', 'Celsius')
    assert "unsupported conversion" in str(excinfo.value) and "fahrenheit" in str(excinfo.value) and "celsius" in str(excinfo.value)
    assert type(excinfo.value) is not ValueError

def test_unsupported_conversion_different_dimensions():
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'kilometers', 'pounds')
    assert "unsupported conversion" in str(excinfo.value) and "kilometers" in str(excinfo.value) and "pounds" in str(excinfo.value)
    assert type(excinfo.value) is not ValueError

def test_unsupported_conversion_to_self():
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'miles', 'miles')
    assert "unsupported conversion" in str(excinfo.value) and "miles" in str(excinfo.value) and "miles" in str(excinfo.value)
    assert type(excinfo.value) is not ValueError

def test_unsupported_conversion_unrecognized():
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'meters', 'feet')
    assert "unsupported conversion" in str(excinfo.value) and "meters" in str(excinfo.value) and "feet" in str(excinfo.value)
    assert type(excinfo.value) is not ValueError

def test_unsupported_conversion_mixed_recognized_and_unrecognized():
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'liters', 'inches')
    assert "unsupported conversion" in str(excinfo.value) and "liters" in str(excinfo.value) and "inches" in str(excinfo.value)
    assert type(excinfo.value) is not ValueError

def test_unsupported_conversion_us_gallons():
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'US gallons', 'liters')
    assert "unsupported conversion" in str(excinfo.value) and "us gallons" in str(excinfo.value) and "liters" in str(excinfo.value)
    assert type(excinfo.value) is not ValueError

def test_unsupported_conversion_uk_gallons():
    with pytest.raises(ValueError) as excinfo:
        convert_units(1, 'UK gallons', 'liters')
    assert "unsupported conversion" in str(excinfo.value) and "uk gallons" in str(excinfo.value) and "liters" in str(excinfo.value)
    assert type(excinfo.value) is not ValueError