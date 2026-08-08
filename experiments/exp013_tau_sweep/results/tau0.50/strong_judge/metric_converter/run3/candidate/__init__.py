class ConversionError(ValueError):
    pass

def convert(value, source_unit, target_unit):
    conversions = {
        'kilometers': {'miles': 0.621371},
        'celsius': {'fahrenheit': (9/5, 32)},
        'kilograms': {'pounds': 1 / 0.45359237},
        'liters': {'us gallons': 1 / 3.785411784, 'uk gallons': 1 / 4.54609}
    }

    source_unit = source_unit.lower()
    target_unit = target_unit.lower()

    if source_unit not in conversions or target_unit not in conversions.get(source_unit, {}):
        raise ConversionError(f"unsupported conversion from '{source_unit}' to '{target_unit}'")

    if source_unit == 'kilometers' and target_unit == 'miles':
        return round(value * conversions[source_unit][target_unit], 6)
    elif source_unit == 'celsius' and target_unit == 'fahrenheit':
        return value * conversions[source_unit][target_unit][0] + conversions[source_unit][target_unit][1]
    elif source_unit == 'kilograms' and target_unit == 'pounds':
        return value * conversions[source_unit][target_unit]
    elif source_unit == 'liters':
        return value * conversions[source_unit][target_unit]
    else:
        raise ConversionError(f"unsupported conversion from '{source_unit}' to '{target_unit}'")
