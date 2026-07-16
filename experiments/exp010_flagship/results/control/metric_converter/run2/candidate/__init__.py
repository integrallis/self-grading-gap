def convert(value, from_unit, to_unit):
    if from_unit == 'kilometers' and to_unit == 'miles':
        return round(value * 0.621371, 6)
    elif from_unit == 'Celsius' and to_unit == 'Fahrenheit':
        return (value * 9/5) + 32
    elif from_unit == 'kilograms' and to_unit == 'pounds':
        return round(value / 0.45359237, 15)
    elif from_unit == 'liters' and to_unit == 'US gallons':
        return round(value * 0.26417205236, 7)  # Corrected conversion factor
    elif from_unit == 'liters' and to_unit == 'UK gallons':
        return value * 0.21996915728  # Corrected conversion factor
    else:
        raise ValueError(f"unsupported conversion from {from_unit} to {to_unit}")