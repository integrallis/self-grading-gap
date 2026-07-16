def convert_units(value, from_unit, to_unit):
    # Conversion factors
    conversions = {
        'kilometers': {'miles': 0.621371},
        'Celsius': {'Fahrenheit': (9/5, 32)},
        'kilograms': {'pounds': 1/0.45359237},
        'liters': {'US gallons': 1/3.785411784, 'UK gallons': 1/4.54609}
    }

    # Check for valid units
    if from_unit not in conversions:
        raise ValueError(f"unsupported conversion from {from_unit} to {to_unit}")
    if to_unit not in conversions[from_unit]:
        raise ValueError(f"unsupported conversion from {from_unit} to {to_unit}")
    if from_unit == to_unit:
        raise ValueError(f"unsupported conversion from {from_unit} to {to_unit}")

    # Perform the conversion
    if from_unit == 'Celsius' and to_unit == 'Fahrenheit':
        return value * conversions[from_unit][to_unit][0] + conversions[from_unit][to_unit][1]
    else:
        return value * conversions[from_unit][to_unit]