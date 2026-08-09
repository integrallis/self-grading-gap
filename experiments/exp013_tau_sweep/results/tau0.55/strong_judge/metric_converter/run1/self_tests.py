# test_solution.py

import pytest
from solution import convert

def test_kilometers_to_miles():
    # 1 km is 0.621371 miles
    assert convert(1, "kilometers", "miles") == pytest.approx(0.621371)
    # 100 km is 62.1371 miles
    assert convert(100, "kilometers", "miles") == pytest.approx(62.1371)
    # 0 km is 0 miles
    assert convert(0, "kilometers", "miles") == pytest.approx(0.0)

def test_celsius_to_fahrenheit():
    # 30 degrees Celsius is (30 * 9/5) + 32 = 86 degrees Fahrenheit
    assert convert(30, "Celsius", "Fahrenheit") == pytest.approx(86.0)
    # 0 degrees Celsius is (0 * 9/5) + 32 = 32 degrees Fahrenheit
    assert convert(0, "Celsius", "Fahrenheit") == pytest.approx(32.0)
    # 100 degrees Celsius is (100 * 9/5) + 32 = 212 degrees Fahrenheit
    assert convert(100, "Celsius", "Fahrenheit") == pytest.approx(212.0)
    # -40 degrees Celsius is (-40 * 9/5) + 32 = -40 degrees Fahrenheit
    assert convert(-40, "Celsius", "Fahrenheit") == pytest.approx(-40.0)

def test_kilograms_to_pounds():
    # 1 kg is 1 / 0.45359237 pounds
    assert convert(1, "kilograms", "pounds") == pytest.approx(2.2046226218487757)
    # 5 kg is 5 / 0.45359237 pounds ≈ 11.023113109243878
    assert convert(5, "kilograms", "pounds") == pytest.approx(5 / 0.45359237)

def test_liters_to_us_gallons():
    # 3.785411784 liters is exactly 1 US gallon
    assert convert(3.785411784, "liters", "US gallons") == pytest.approx(1.0)

def test_liters_to_uk_gallons():
    # 4.54609 liters is exactly 1 UK gallon
    assert convert(4.54609, "liters", "UK gallons") == pytest.approx(1.0)

def test_liters_to_gallons_difference():
    # 4.54609 liters is 1 UK gallon and 3.785411784 liters is 1 US gallon
    assert convert(4.54609, "liters", "UK gallons") < convert(4.54609, "liters", "US gallons")

def test_unsupported_conversion_reverse_direction_miles():
    # Converting miles to kilometers is unsupported
    with pytest.raises(ValueError) as excinfo:
        convert(1, "miles", "kilometers")
    assert isinstance(excinfo.value, ValueError)
    assert "unsupported conversion" in str(excinfo.value)
    assert "miles" in str(excinfo.value)
    assert "kilometers" in str(excinfo.value)

def test_unsupported_conversion_reverse_direction_fahrenheit():
    # Converting Fahrenheit to Celsius is unsupported
    with pytest.raises(ValueError) as excinfo:
        convert(1, "Fahrenheit", "Celsius")
    assert isinstance(excinfo.value, ValueError)
    assert "unsupported conversion" in str(excinfo.value)
    assert "fahrenheit" in str(excinfo.value)
    assert "celsius" in str(excinfo.value)

def test_unsupported_conversion_reverse_direction_pounds():
    # Converting pounds to kilograms is unsupported
    with pytest.raises(ValueError) as excinfo:
        convert(1, "pounds", "kilograms")
    assert isinstance(excinfo.value, ValueError)
    assert "unsupported conversion" in str(excinfo.value)
    assert "pounds" in str(excinfo.value)
    assert "kilograms" in str(excinfo.value)

def test_unsupported_conversion_reverse_direction_us_gallons():
    # Converting US gallons to liters is unsupported
    with pytest.raises(ValueError) as excinfo:
        convert(1, "US gallons", "liters")
    assert isinstance(excinfo.value, ValueError)
    assert "unsupported conversion" in str(excinfo.value)
    assert "us gallons" in str(excinfo.value)
    assert "liters" in str(excinfo.value)

def test_unsupported_conversion_reverse_direction_uk_gallons():
    # Converting UK gallons to liters is unsupported
    with pytest.raises(ValueError) as excinfo:
        convert(1, "UK gallons", "liters")
    assert isinstance(excinfo.value, ValueError)
    assert "unsupported conversion" in str(excinfo.value)
    assert "uk gallons" in str(excinfo.value)
    assert "liters" in str(excinfo.value)

def test_unsupported_conversion_different_dimensions():
    # Converting kilometers to pounds is unsupported
    with pytest.raises(ValueError) as excinfo:
        convert(1, "kilometers", "pounds")
    assert isinstance(excinfo.value, ValueError)
    assert "unsupported conversion" in str(excinfo.value)
    assert "kilometers" in str(excinfo.value)
    assert "pounds" in str(excinfo.value)

def test_unsupported_conversion_to_self():
    # Converting kilometers to kilometers is unsupported
    with pytest.raises(ValueError) as excinfo:
        convert(1, "kilometers", "kilometers")
    assert isinstance(excinfo.value, ValueError)
    assert "unsupported conversion" in str(excinfo.value)
    assert "kilometers" in str(excinfo.value)
    assert "kilometers" in str(excinfo.value)

def test_unsupported_conversion_unrecognized_units():
    # Converting unrecognized units should raise an error
    with pytest.raises(ValueError) as excinfo:
        convert(1, "foo", "bar")
    assert isinstance(excinfo.value, ValueError)
    assert "unsupported conversion" in str(excinfo.value)
    assert "foo" in str(excinfo.value)
    assert "bar" in str(excinfo.value)

def test_unsupported_conversion_with_recognized_unit():
    # Converting unrecognized units to recognized units should raise an error
    with pytest.raises(ValueError) as excinfo:
        convert(1, "meters", "miles")
    assert isinstance(excinfo.value, ValueError)
    assert "unsupported conversion" in str(excinfo.value)
    assert "meters" in str(excinfo.value)
    assert "miles" in str(excinfo.value)

# Parameterized tests for additional supported formulas
@pytest.mark.parametrize("km, expected_miles", [
    (2.5, 2.5 * 0.621371),
    (10, 10 * 0.621371),
    (50, 50 * 0.621371),
])
def test_parameterized_kilometers_to_miles(km, expected_miles):
    assert convert(km, "kilometers", "miles") == pytest.approx(expected_miles)

@pytest.mark.parametrize("celsius, expected_fahrenheit", [
    (-17, (-17 * 9/5) + 32),
    (25, (25 * 9/5) + 32),
    (37, (37 * 9/5) + 32),
])
def test_parameterized_celsius_to_fahrenheit(celsius, expected_fahrenheit):
    assert convert(celsius, "Celsius", "Fahrenheit") == pytest.approx(expected_fahrenheit)

@pytest.mark.parametrize("kg, expected_pounds", [
    (3.2, 3.2 / 0.45359237),
    (7, 7 / 0.45359237),
])
def test_parameterized_kilograms_to_pounds(kg, expected_pounds):
    assert convert(kg, "kilograms", "pounds") == pytest.approx(expected_pounds)

@pytest.mark.parametrize("liters, expected_us_gallons", [
    (5, 5 / 3.785411784),
    (10, 10 / 3.785411784),
])
def test_parameterized_liters_to_us_gallons(liters, expected_us_gallons):
    assert convert(liters, "liters", "US gallons") == pytest.approx(expected_us_gallons)

@pytest.mark.parametrize("liters, expected_uk_gallons", [
    (5, 5 / 4.54609),
    (10, 10 / 4.54609),
])
def test_parameterized_liters_to_uk_gallons(liters, expected_uk_gallons):
    assert convert(liters, "liters", "UK gallons") == pytest.approx(expected_uk_gallons)