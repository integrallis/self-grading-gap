def convert_units(value, from_unit, to_unit):
    class ConversionError(ValueError):
        pass

    # Distance conversions
    if from_unit == 'kilometers' and to_unit == 'miles':
        return value * 0.621371
    elif from_unit == 'miles' and to_unit == 'kilometers':
        raise ConversionError(f"unsupported conversion from '{from_unit.lower()}' to '{to_unit.lower()}'")

    # Temperature conversions
    elif from_unit == 'Celsius' and to_unit == 'Fahrenheit':
        return (value * 9/5) + 32
    elif from_unit == 'Fahrenheit' and to_unit == 'Celsius':
        raise ConversionError(f"unsupported conversion from '{from_unit.lower()}' to '{to_unit.lower()}'")

    # Mass conversions
    elif from_unit == 'kilograms' and to_unit == 'pounds':
        return value / 0.45359237
    elif from_unit == 'pounds' and to_unit == 'kilograms':
        raise ConversionError(f"unsupported conversion from '{from_unit.lower()}' to '{to_unit.lower()}'")

    # Volume conversions
    elif from_unit == 'liters' and to_unit == 'US gallons':
        return value / 3.785411784
    elif from_unit == 'liters' and to_unit == 'UK gallons':
        return value / 4.54609
    elif from_unit in ['US gallons', 'UK gallons']:
        raise ConversionError(f"unsupported conversion from '{from_unit.lower()}' to '{to_unit.lower()}'")

    # Unsupported conversions
    else:
        raise ConversionError(f"unsupported conversion from '{from_unit.lower()}' to '{to_unit.lower()}'")
