import pytest

def register_suppliers(suppliers):
    if len(suppliers) < 3:
        raise ValueError(f"at least 3 suppliers are required, got {len(suppliers)}")
    names = set()
    for name, _ in suppliers:
        if name in names:
            raise ValueError(f"duplicate supplier name {name}")
        names.add(name)


def quote_robot(suppliers, config):
    parts = []
    total = 0
    for category, option in config.items():
        best_supplier = None
        best_price = float('inf')
        for name, offerings in suppliers:
            if category in offerings and option in offerings[category]:
                price = offerings[category][option]
                if price < best_price:
                    best_price = price
                    best_supplier = name
                elif price == best_price:  # tie-breaking
                    continue  # first registered stays
        if best_supplier is None:
            raise ValueError(f"no supplier carries {option} for {category}")
        parts.append({"category": category, "supplier": best_supplier, "price": best_price})
        total += best_price
    return {"parts": parts, "total": total}


def validate_configuration(config):
    required_parts = ["head", "body", "arms", "movement", "power"]
    for part in required_parts:
        if part not in config:
            raise ValueError(f"missing part category {part}")
    for category, option in config.items():
        if category not in required_parts:
            raise ValueError(f"unknown part category {category}")
        # Assume suppliers are available in the context
        for name, offerings in suppliers:
            if category in offerings and option not in offerings[category]:
                raise ValueError(f"invalid {category} option {option}")


def purchase_robot(quote):
    if isinstance(quote, str):
        raise ValueError(f"unknown supplier {quote}")
    orders = {}
    for part in quote['parts']:
        supplier = part['supplier']
        if supplier not in orders:
            orders[supplier] = []
        orders[supplier].append({"option": part['category'], "price": part['price'], "category": part['category']})
    return {"orders": orders, "total": quote['total'], "parts": quote['parts']}