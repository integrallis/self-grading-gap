import pytest
from solution import convert

# US-1: Distance tests
def test_kilometers_to_miles():
    assert convert(1, "kilometers", "miles") == 0.621371  # 1 km = 0.621371 miles
    assert convert(100, "kilometers", "miles") == 62.1371  # 100 km = 62.1371 miles
    assert convert(0, "kilometers", "miles") == 0.0  # 0 km = 0 miles

# US-2: Temperature tests
def test_celsius_to_fahrenheit():
    assert convert(30, "Celsius", "Fahrenheit") == 86.0  # 30°C = (30 * 9/5) + 32 = 86°F
    assert convert(0, "Celsius", "Fahrenheit") == 32.0  # 0°C = 32°F
    assert convert(100, "Celsius", "Fahrenheit") == 212.0  # 100°C = 212°F
    assert convert(-40, "Celsius", "Fahrenheit") == -40.0  # -40°C = -40°F

# US-3: Mass tests
def test_kilograms_to_pounds():
    assert convert(1, "kilograms", "pounds") == 2.2046226218487757  # 1 kg = 1 / 0.45359237 pounds
    assert abs(convert(5, "kilograms", "pounds") - (5 / 0.45359237)) < 1e-9  # 5 kg ≈ 11.023113109243878 pounds

# US-4: Volume tests
def test_liters_to_gallons():
    assert convert(3.785411784, "liters", "US gallons") == 1.0  # 3.785411784 liters = 1 US gallon
    assert convert(4.54609, "liters", "UK gallons") == 1.0  # 4.54609 liters = 1 UK gallon
    assert convert(4.54609, "liters", "UK gallons") < convert(4.54609, "liters", "US gallons")  # UK gallons < US gallons

# US-5: Guarding the supported set tests
def test_unsupported_conversion_reverse():
    with pytest.raises(ValueError) as exc:
        convert(1, "miles", "kilometers")
    assert "unsupported conversion" in str(exc.value)
    assert "miles" in str(exc.value)
    assert "kilometers" in str(exc.value)

def test_unsupported_conversion_different_dimensions():
    with pytest.raises(ValueError) as exc:
        convert(1, "kilometers", "pounds")
    assert "unsupported conversion" in str(exc.value)
    assert "kilometers" in str(exc.value)
    assert "pounds" in str(exc.value)

def test_unsupported_conversion_same_unit():
    with pytest.raises(ValueError) as exc:
        convert(1, "liters", "liters")
    assert "unsupported conversion" in str(exc.value)
    assert "liters" in str(exc.value)
    assert "liters" in str(exc.value)

def test_unsupported_conversion_unknown_source():
    with pytest.raises(ValueError) as exc:
        convert(1, "unknown", "miles")
    assert "unsupported conversion" in str(exc.value)
    assert "unknown" in str(exc.value)
    assert "miles" in str(exc.value)

def test_unsupported_conversion_unknown_destination():
    with pytest.raises(ValueError) as exc:
        convert(1, "kilometers", "unknown")
    assert "unsupported conversion" in str(exc.value)
    assert "kilometers" in str(exc.value)
    assert "unknown" in str(exc.value)

def test_unsupported_conversion_unknown_units():
    with pytest.raises(ValueError) as exc:
        convert(1, "unknown", "unknown")
    assert "unsupported conversion" in str(exc.value)
    assert "unknown" in str(exc.value)
    assert "unknown" in str(exc.value)

# Additional tests for unsupported conversion exceptions
def test_unsupported_conversion_fahrenheit_to_celsius():
    with pytest.raises(ValueError) as exc:
        convert(32, "Fahrenheit", "Celsius")
    assert "unsupported conversion" in str(exc.value)
    assert "fahrenheit" in str(exc.value)
    assert "celsius" in str(exc.value)

def test_unsupported_conversion_pounds_to_kilograms():
    with pytest.raises(ValueError) as exc:
        convert(1, "pounds", "kilograms")
    assert "unsupported conversion" in str(exc.value)
    assert "pounds" in str(exc.value)
    assert "kilograms" in str(exc.value)

def test_unsupported_conversion_us_gallons_to_liters():
    with pytest.raises(ValueError) as exc:
        convert(1, "US gallons", "liters")
    assert "unsupported conversion" in str(exc.value)
    assert "us gallons" in str(exc.value)
    assert "liters" in str(exc.value)

def test_unsupported_conversion_uk_gallons_to_liters():
    with pytest.raises(ValueError) as exc:
        convert(1, "UK gallons", "liters")
    assert "unsupported conversion" in str(exc.value)
    assert "uk gallons" in str(exc.value)
    assert "liters" in str(exc.value)