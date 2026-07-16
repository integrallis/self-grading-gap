def register_suppliers(suppliers):
    names = set()
    if len(suppliers) < 3:
        raise ValueError(f"at least 3 suppliers are required, got {len(suppliers)}")
    for name, parts in suppliers:
        if name in names:
            raise ValueError(f"duplicate supplier name {name}")
        names.add(name)
    global SUPPLIERS
    SUPPLIERS = suppliers


def quote_robot(config):
    validate_configuration(config)
    parts = []
    total = 0
    for category in ["head", "body", "arms", "movement", "power"]:
        option = config.get(category)
        supplier_name = None
        price = 0
        for name, parts_dict in SUPPLIERS:
            if category in parts_dict and option in parts_dict[category]:
                part_price = parts_dict[category][option]
                if supplier_name is None or part_price < price:
                    supplier_name = name
                    price = part_price
        # If no supplier found, default price is 0
        parts.append({"category": category, "supplier": supplier_name, "price": price})
        total += price
    return {"parts": parts, "total": total}


def validate_configuration(config):
    required_parts = ["head", "body", "arms", "movement", "power"]
    for part in required_parts:
        if part not in config:
            raise ValueError(f"missing part category {part}")
    known_parts = set()
    for name, parts_dict in SUPPLIERS:
        for part, options in parts_dict.items():
            known_parts.update(options.keys())
    for part, option in config.items():
        if part not in required_parts:
            raise ValueError(f"unknown part category {part}")
        if option not in known_parts:
            raise ValueError(f"invalid {part} option {option}")
        if not any(option in parts_dict.get(part, {}) for _, parts_dict in SUPPLIERS):
            raise ValueError(f"no supplier carries {option}")


def purchase_robot(quote):
    if quote is None:
        raise ValueError("No quote to purchase")
    orders = []
    for part in quote['parts']:
        supplier = part['supplier']
        if supplier is None:
            continue
        price = part['price']
        orders.append({"supplier": supplier, "option": part['category'], "price": price})
    serial_name = generate_serial_name()
    return {"orders": orders, "serial_name": serial_name}


def generate_serial_name():
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase, k=2)) + ''.join(random.choices(string.digits, k=3))