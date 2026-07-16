# file: metric_converter.py
from candidate import convert_units as convert


UnsupportedConversionError = ValueError


class Unit:
    KILOMETERS = "kilometers"
    MILES = "miles"
    CELSIUS = "Celsius"
    FAHRENHEIT = "Fahrenheit"
    KILOGRAMS = "kilograms"
    POUNDS = "pounds"
    LITERS = "liters"
    US_GALLONS = "US gallons"
    UK_GALLONS = "UK gallons"
