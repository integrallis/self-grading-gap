def convert_units(value, from_unit, to_unit):
    # Conversion factors
    conversion_factors = {
        'kilometers': {'miles': 0.621371},
        'Celsius': {'Fahrenheit': lambda c: (c * 9/5) + 32},
        'kilograms': {'pounds': 2.2046226218487757},
        'liters': {'US gallons': 3.785411784, 'UK gallons': 4.54609}
    }

    # Validate units
    if from_unit not in conversion_factors:
        raise ValueError(f"unsupported conversion from '{from_unit}' to '{to_unit}'")
    if to_unit not in conversion_factors[from_unit]:
        raise ValueError(f"unsupported conversion from '{from_unit}' to '{to_unit}'")

    # Perform conversion
    if callable(conversion_factors[from_unit][to_unit]):
        return conversion_factors[from_unit][to_unit](value)
    else:
        return round(value / conversion_factors[from_unit][to_unit], 4)
