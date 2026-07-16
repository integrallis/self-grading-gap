import pytest
from solution import convert_units  # Assuming this is the function we will implement

# US-1: Distance
def test_kilometers_to_miles():
    assert convert_units(1, 'kilometers', 'miles') == 0.621371  # 1 km = 0.621371 miles
    assert convert_units(100, 'kilometers', 'miles') == pytest.approx(62.1371)  # 100 km = 100 * 0.621371 miles

def test_zero_kilometers_to_miles():
    assert convert_units(0, 'kilometers', 'miles') == 0  # 0 km = 0 miles

# US-2: Temperature
def test_celsius_to_fahrenheit():
    assert convert_units(30, 'Celsius', 'Fahrenheit') == 86  # 30 C = (30 * 9/5) + 32 = 86 F

def test_freezing_point_celsius_to_fahrenheit():
    assert convert_units(0, 'Celsius', 'Fahrenheit') == 32  # 0 C = 32 F

def test_boiling_point_celsius_to_fahrenheit():
    assert convert_units(100, 'Celsius', 'Fahrenheit') == 212  # 100 C = 212 F

def test_crossover_point():
    assert convert_units(-40, 'Celsius', 'Fahrenheit') == -40  # -40 C = -40 F

# US-3: Mass
def test_kilograms_to_pounds():
    assert convert_units(1, 'kilograms', 'pounds') == pytest.approx(2.2046226218487757)  # 1 kg = 1 / 0.45359237 pounds
    assert convert_units(5, 'kilograms', 'pounds') == pytest.approx(11.023113109243878)  # 5 kg = 5 / 0.45359237 pounds

# US-4: Volume
def test_liters_to_us_gallons():
    assert convert_units(3.785411784, 'liters', 'US gallons') == 1  # 3.785411784 L = 1 US gallon

def test_liters_to_uk_gallons():
    assert convert_units(4.54609, 'liters', 'UK gallons') == 1  # 4.54609 L = 1 UK gallon

def test_liters_to_different_gallons():
    assert convert_units(3.785411784, 'liters', 'UK gallons') < convert_units(3.785411784, 'liters', 'US gallons')  # UK gallons < US gallons for the same volume

# US-5: Guarding the supported set
def test_unsupported_conversion_reverse_km_to_miles():
    with pytest.raises(ValueError) as e:
        convert_units(1, 'miles', 'kilometers')
    assert "unsupported conversion" in str(e.value) and "miles" in str(e.value) and "kilometers" in str(e.value)
    assert type(e.value) is not ValueError

def test_unsupported_conversion_reverse_fahrenheit_to_celsius():
    with pytest.raises(ValueError) as e:
        convert_units(1, 'Fahrenheit', 'Celsius')
    assert "unsupported conversion" in str(e.value) and "fahrenheit" in str(e.value) and "celsius" in str(e.value)
    assert type(e.value) is not ValueError

def test_unsupported_conversion_different_dimensions():
    with pytest.raises(ValueError) as e:
        convert_units(1, 'kilometers', 'pounds')
    assert "unsupported conversion" in str(e.value) and "kilometers" in str(e.value) and "pounds" in str(e.value)
    assert type(e.value) is not ValueError

def test_unsupported_conversion_same_units():
    with pytest.raises(ValueError) as e:
        convert_units(1, 'liters', 'liters')
    assert "unsupported conversion" in str(e.value) and "liters" in str(e.value) and "liters" in str(e.value)
    assert type(e.value) is not ValueError

def test_unsupported_conversion_unrecognized_units():
    with pytest.raises(ValueError) as e:
        convert_units(1, 'meters', 'inches')
    assert "unsupported conversion" in str(e.value) and "meters" in str(e.value) and "inches" in str(e.value)
    assert type(e.value) is not ValueError

def test_unsupported_conversion_reverse_pounds_to_kilograms():
    with pytest.raises(ValueError) as e:
        convert_units(1, 'pounds', 'kilograms')
    assert "unsupported conversion" in str(e.value) and "pounds" in str(e.value) and "kilograms" in str(e.value)
    assert type(e.value) is not ValueError

def test_unsupported_conversion_reverse_us_gallons_to_liters():
    with pytest.raises(ValueError) as e:
        convert_units(1, 'US gallons', 'liters')
    assert "unsupported conversion" in str(e.value) and "us gallons" in str(e.value) and "liters" in str(e.value)
    assert type(e.value) is not ValueError

def test_unsupported_conversion_reverse_uk_gallons_to_liters():
    with pytest.raises(ValueError) as e:
        convert_units(1, 'UK gallons', 'liters')
    assert "unsupported conversion" in str(e.value) and "uk gallons" in str(e.value) and "liters" in str(e.value)
    assert type(e.value) is not ValueError