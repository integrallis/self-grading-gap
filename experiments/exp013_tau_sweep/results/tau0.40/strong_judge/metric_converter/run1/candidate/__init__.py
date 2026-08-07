class UnsupportedConversionError(ValueError): pass

def convert_units(value, source, target):
    # Define conversion factors
    conversions = {
        'kilometers': {'miles': 0.621371},
        'celsius': {'fahrenheit': lambda c: c * 9/5 + 32},
        'kilograms': {'pounds': 1 / 0.45359237},
        'liters': {'us gallons': 1 / 3.785411784, 'uk gallons': 1 / 4.54609}
    }

    # Normalize input
    source = source.lower()
    target = target.lower()

    # Check for self-conversion
    if source == target:
        raise UnsupportedConversionError(f'unsupported conversion: {source} to {target}')

    # Check if source unit exists
    if source not in conversions:
        raise UnsupportedConversionError(f'unsupported conversion: {source} to {target}')

    # Check if target unit exists in the source conversion map
    if target not in conversions[source]:
        raise UnsupportedConversionError(f'unsupported conversion: {source} to {target}')

    # Perform conversion
    conversion = conversions[source][target]
    if callable(conversion):  # Handle functions (like Celsius to Fahrenheit)
        return conversion(value)
    return value * conversion
