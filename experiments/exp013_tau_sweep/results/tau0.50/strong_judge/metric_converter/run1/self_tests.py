import pytest
from solution import convert

# US-1: Distance
def test_kilometers_to_miles():
    assert convert(1, "kilometers", "miles") == 0.621371  # 1 km * 0.621371 miles/km
    assert convert(100, "kilometers", "miles") == 62.1371  # 100 km * 0.621371 miles/km
    assert convert(0, "kilometers", "miles") == 0.0  # 0 km * 0.621371 miles/km

# US-2: Temperature
def test_celsius_to_fahrenheit():
    assert convert(30, "celsius", "fahrenheit") == 86.0  # (30 * 9/5) + 32
    assert convert(0, "celsius", "fahrenheit") == 32.0  # (0 * 9/5) + 32
    assert convert(100, "celsius", "fahrenheit") == 212.0  # (100 * 9/5) + 32
    assert convert(-40, "celsius", "fahrenheit") == -40.0  # (-40 * 9/5) + 32

# US-3: Mass
def test_kilograms_to_pounds():
    assert convert(1, "kilograms", "pounds") == 2.2046226218487757  # 1 kg / 0.45359237
    assert convert(5, "kilograms", "pounds") == 11.023113109243878  # 5 kg / 0.45359237

# US-4: Volume
def test_liters_to_gallons():
    assert convert(3.785411784, "liters", "US gallons") == 1.0  # 3.785411784 L = 1 US gallon
    assert convert(4.54609, "liters", "UK gallons") == 1.0  # 4.54609 L = 1 UK gallon
    assert convert(4.54609, "liters", "UK gallons") < convert(4.54609, "liters", "US gallons")  # UK gallons < US gallons

# US-5: Guarding the supported set
def test_unsupported_conversions():
    with pytest.raises(ValueError) as excinfo:
        convert(1, "miles", "kilometers")
    assert "unsupported conversion" in str(excinfo.value)
    assert "miles" in str(excinfo.value).lower()
    assert "kilometers" in str(excinfo.value).lower()

    with pytest.raises(ValueError) as excinfo:
        convert(32, "fahrenheit", "celsius")
    assert "unsupported conversion" in str(excinfo.value)
    assert "fahrenheit" in str(excinfo.value).lower()
    assert "celsius" in str(excinfo.value).lower()

    with pytest.raises(ValueError) as excinfo:
        convert(1, "kilometers", "pounds")
    assert "unsupported conversion" in str(excinfo.value)
    assert "kilometers" in str(excinfo.value).lower()
    assert "pounds" in str(excinfo.value).lower()

    with pytest.raises(ValueError) as excinfo:
        convert(1, "kilograms", "kilograms")
    assert "unsupported conversion" in str(excinfo.value)
    assert "kilograms" in str(excinfo.value).lower()
    assert "kilograms" in str(excinfo.value).lower()

    with pytest.raises(ValueError) as excinfo:
        convert(1, "liters", "liters")
    assert "unsupported conversion" in str(excinfo.value)
    assert "liters" in str(excinfo.value).lower()
    assert "liters" in str(excinfo.value).lower()

    with pytest.raises(ValueError) as excinfo:
        convert(1, "meters", "miles")  # Testing an unrecognized unit
    assert "unsupported conversion" in str(excinfo.value)
    assert "meters" in str(excinfo.value).lower()
    assert "miles" in str(excinfo.value).lower()

    with pytest.raises(ValueError) as excinfo:
        convert(1, "pounds", "kilograms")
    assert "unsupported conversion" in str(excinfo.value)
    assert "pounds" in str(excinfo.value).lower()
    assert "kilograms" in str(excinfo.value).lower()

    with pytest.raises(ValueError) as excinfo:
        convert(1, "US gallons", "liters")
    assert "unsupported conversion" in str(excinfo.value)
    assert "us gallons" in str(excinfo.value).lower()
    assert "liters" in str(excinfo.value).lower()

    with pytest.raises(ValueError) as excinfo:
        convert(1, "UK gallons", "liters")
    assert "unsupported conversion" in str(excinfo.value)
    assert "uk gallons" in str(excinfo.value).lower()
    assert "liters" in str(excinfo.value).lower()

    with pytest.raises(ValueError) as excinfo:
        convert(1, "kilograms", "liters")
    assert "unsupported conversion" in str(excinfo.value)
    assert "kilograms" in str(excinfo.value).lower()
    assert "liters" in str(excinfo.value).lower()