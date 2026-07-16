def register_suppliers(suppliers):
    if len(suppliers) < 3:
        raise ValueError(f"at least 3 suppliers are required, got {len(suppliers)}")
    names = set()
    for supplier in suppliers:
        if not isinstance(supplier, tuple) or len(supplier) != 2:
            raise ValueError("Each supplier must be a tuple of (name, part_dict)")
        name, parts = supplier
        if name in names:
            raise ValueError(f"duplicate supplier name {name}")
        names.add(name)
    global registered_suppliers
    registered_suppliers = suppliers


def quote_robot(configuration):
    validate_configuration(configuration)
    parts = []
    total = 0
    for category, option in configuration.items():
        cheapest = None
        for supplier_name, parts_dict in registered_suppliers:
            if category in parts_dict and option in parts_dict[category]:
                price = parts_dict[category][option]
                if cheapest is None or price < cheapest['price']:
                    cheapest = {'supplier': supplier_name, 'price': price, 'category': category}
        parts.append({'category': category, 'supplier': cheapest['supplier'], 'price': cheapest['price']})
        total += cheapest['price']
    return {'parts': parts, 'total': total}


def validate_configuration(configuration):
    required_categories = {'head', 'body', 'arms', 'movement', 'power'}
    provided_categories = set(configuration.keys())
    missing = required_categories - provided_categories
    if missing:
        raise ValueError(f"missing part category {', '.join(missing)}")
    unknown = provided_categories - required_categories
    if unknown:
        raise ValueError(f"unknown part category {', '.join(unknown)}")
    for category, option in configuration.items():
        if option not in [opt for name, parts in registered_suppliers for opt in parts[category]]:
            raise ValueError(f"invalid {category} option {option}")


def purchase_robot(quote):
    global order_history
    if 'order_history' not in globals():
        order_history = {}
    for part in quote['parts']:
        supplier = part['supplier']
        if supplier not in order_history:
            order_history[supplier] = []
        order_history[supplier].append({'category': part['category'], 'option': part['option'], 'price': part['price']})
    return {'parts': quote['parts'], 'total': quote['total'], 'serial_name': generate_serial_name()}


def get_order_history(supplier):
    if supplier not in order_history:
        raise ValueError(f"unknown supplier {supplier}")
    return order_history[supplier]


def generate_serial_name():
    import random
    import string
    serial = ''.join(random.choices(string.ascii_uppercase, k=2)) + ''.join(random.choices(string.digits, k=3))
    return serial

registered_suppliers = []
order_history = {}