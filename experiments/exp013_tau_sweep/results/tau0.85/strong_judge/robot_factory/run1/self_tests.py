import pytest
import re
from solution import register_suppliers, quote_robot, validate_configuration, purchase_robot

def test_register_suppliers_rejects_fewer_than_three_suppliers():
    with pytest.raises(Exception) as excinfo:  # Check for generic Exception since specific type is not defined
        register_suppliers([{"name": "Supplier A"}, {"name": "Supplier B"}])
    assert str(excinfo.value) == "at least 3 suppliers are required, got 2"

def test_register_suppliers_rejects_duplicate_supplier_names():
    with pytest.raises(Exception) as excinfo:  # Check for generic Exception since specific type is not defined
        register_suppliers([{"name": "Supplier A"}, {"name": "Supplier A"}, {"name": "Supplier C"}])
    assert str(excinfo.value) == "duplicate supplier name Supplier A"

def test_register_suppliers_accepts_valid_supplier_pool():
    result = register_suppliers([
        {"name": "Supplier A"},
        {"name": "Supplier B"},
        {"name": "Supplier C"}
    ])
    assert result is None  # Assuming successful registration returns None

def test_quote_robot_sources_parts_from_lowest_price_supplier():
    suppliers = [
        {"name": "Supplier A", "head": {"standard vision": 10}, "body": {"square": 20}, "arms": {"hands": 15}, "movement": {"wheels": 25}, "power": {"solar": 5}},
        {"name": "Supplier B", "head": {"standard vision": 12, "body": {"square": 18}, "arms": {"hands": 14}, "movement": {"wheels": 24}, "power": {"solar": 4}}},
        {"name": "Supplier C", "head": {"standard vision": 11, "body": {"round": 22}, "arms": {"hands": 16}, "movement": {"legs": 20}, "power": {"solar": 6}}}
    ]
    quote = quote_robot(suppliers, {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    assert quote['parts']['head'] == {"category": "head", "supplier": "Supplier A", "price": 10}
    assert quote['parts']['body'] == {"category": "body", "supplier": "Supplier A", "price": 20}
    assert quote['parts']['arms'] == {"category": "arms", "supplier": "Supplier A", "price": 15}
    assert quote['parts']['movement'] == {"category": "movement", "supplier": "Supplier A", "price": 25}
    assert quote['parts']['power'] == {"category": "power", "supplier": "Supplier A", "price": 5}

def test_quote_robot_total_is_sum_of_parts_prices():
    suppliers = [
        {"name": "Supplier A", "head": {"standard vision": 10}, "body": {"square": 20}, "arms": {"hands": 15}, "movement": {"wheels": 25}, "power": {"solar": 5}},
        {"name": "Supplier B", "head": {"standard vision": 12, "body": {"square": 18}, "arms": {"hands": 14}, "movement": {"wheels": 24}, "power": {"solar": 4}}}
    ]
    quote = quote_robot(suppliers, {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    total = 10 + 20 + 15 + 25 + 5  # Sum of all prices from suppliers
    assert quote['total'] == total

def test_quote_robot_ties_on_price_first_supplier_wins():
    suppliers = [
        {"name": "Supplier A", "body": {"square": 20}, "power": {"solar": 5}},
        {"name": "Supplier B", "body": {"square": 20}, "power": {"solar": 4}},
        {"name": "Supplier C", "head": {"standard vision": 10}}
    ]
    quote = quote_robot(suppliers, {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    assert quote['parts']['body'] == {"category": "body", "supplier": "Supplier A", "price": 20}  # First supplier wins tie

def test_quote_robot_sources_parts_from_multiple_suppliers():
    suppliers = [
        {"name": "Supplier A", "head": {"standard vision": 10}, "arms": {"hands": 15}},
        {"name": "Supplier B", "body": {"square": 20}, "movement": {"wheels": 10}},
        {"name": "Supplier C", "power": {"solar": 5}}
    ]
    quote = quote_robot(suppliers, {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    assert quote['parts']['head'] == {"category": "head", "supplier": "Supplier A", "price": 10}
    assert quote['parts']['body'] == {"category": "body", "supplier": "Supplier B", "price": 20}
    assert quote['parts']['arms'] == {"category": "arms", "supplier": "Supplier A", "price": 15}
    assert quote['parts']['movement'] == {"category": "movement", "supplier": "Supplier B", "price": 10}
    assert quote['parts']['power'] == {"category": "power", "supplier": "Supplier C", "price": 5}

def test_validate_configuration_rejects_missing_part_category():
    with pytest.raises(Exception) as excinfo:  # Check for generic Exception since specific type is not defined
        validate_configuration({"head": "standard vision", "body": "square", "arms": "hands", "power": "solar"})
    assert str(excinfo.value) == "missing part category movement"

def test_validate_configuration_rejects_unknown_part_category():
    with pytest.raises(Exception) as excinfo:  # Check for generic Exception since specific type is not defined
        validate_configuration({"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar", "wings": "none"})
    assert str(excinfo.value) == "unknown part category wings"

def test_validate_configuration_rejects_invalid_option_for_category():
    with pytest.raises(Exception) as excinfo:  # Check for generic Exception since specific type is not defined
        validate_configuration({"head": "unknown vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    assert str(excinfo.value) == "invalid head option unknown vision"

def test_validate_configuration_rejects_option_with_no_supplier():
    suppliers = [
        {"name": "Supplier A", "head": {"standard vision": 10}, "body": {"square": 20}, "arms": {"hands": 15}, "movement": {"wheels": 25}, "power": {"solar": 5}}
    ]
    with pytest.raises(Exception) as excinfo:  # Check for generic Exception
        validate_configuration({"head": "infrared vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"}, suppliers)
    assert str(excinfo.value) == "no supplier carries infrared vision"

def test_purchase_robot_records_order_with_correct_parts():
    suppliers = [
        {"name": "Supplier A", "head": {"standard vision": 10}, "arms": {"hands": 15}},
        {"name": "Supplier B", "body": {"square": 20}, "movement": {"wheels": 10}},
        {"name": "Supplier C", "power": {"solar": 5}}
    ]
    quote = quote_robot(suppliers, {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    purchase = purchase_robot(quote, suppliers)
    assert purchase['orders'] == [
        {"supplier": "Supplier A", "option": "standard vision", "price": 10},
        {"supplier": "Supplier B", "option": "square", "price": 20},
        {"supplier": "Supplier A", "option": "hands", "price": 15},
        {"supplier": "Supplier B", "option": "wheels", "price": 10},
        {"supplier": "Supplier C", "option": "solar", "price": 5}
    ]

def test_purchase_robot_total_matches_quote():
    suppliers = [
        {"name": "Supplier A", "head": {"standard vision": 10}, "arms": {"hands": 15}},
        {"name": "Supplier B", "body": {"square": 20}, "movement": {"wheels": 10}},
        {"name": "Supplier C", "power": {"solar": 5}}
    ]
    quote = quote_robot(suppliers, {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    purchase = purchase_robot(quote, suppliers)
    assert purchase['total'] == quote['total']  # Ensure total matches

def test_purchase_robot_records_no_orders_if_only_quoted():
    suppliers = [
        {"name": "Supplier A", "head": {"standard vision": 10}},
        {"name": "Supplier B", "body": {"square": 20}},
        {"name": "Supplier C", "power": {"solar": 5}}
    ]
    quote = quote_robot(suppliers, {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    purchase = purchase_robot(quote, suppliers)
    assert purchase['orders'] == []  # Should not have any orders

def test_purchase_robot_rejects_unknown_supplier_history_request():
    with pytest.raises(Exception) as excinfo:  # Check for generic Exception
        purchase_robot({"supplier": "Unknown"}, [])
    assert str(excinfo.value) == "unknown supplier Unknown"

def test_purchased_robot_serial_name_format():
    suppliers = [
        {"name": "Supplier A", "head": {"standard vision": 10}, "arms": {"hands": 15}},
        {"name": "Supplier B", "body": {"square": 20}, "movement": {"wheels": 10}},
        {"name": "Supplier C", "power": {"solar": 5}}
    ]
    quote = quote_robot(suppliers, {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    purchase = purchase_robot(quote, suppliers)
    assert re.match(r'^[A-Z]{2}\d{3}$', purchase['serial_name'])  # Each name must match the format

def test_purchased_robot_serial_names_are_unique():
    suppliers = [
        {"name": "Supplier A", "head": {"standard vision": 10}, "arms": {"hands": 15}},
        {"name": "Supplier B", "body": {"square": 20}, "movement": {"wheels": 10}},
        {"name": "Supplier C", "power": {"solar": 5}}
    ]
    quote1 = quote_robot(suppliers, {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    purchase1 = purchase_robot(quote1, suppliers)

    quote2 = quote_robot(suppliers, {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    purchase2 = purchase_robot(quote2, suppliers)

    assert purchase1['serial_name'] != purchase2['serial_name']  # Ensure serial names are unique

def test_purchased_robot_serial_names_are_reproducible():
    # This test assumes that the randomness source is seeded and deterministic
    suppliers = [
        {"name": "Supplier A", "head": {"standard vision": 10}, "arms": {"hands": 15}},
        {"name": "Supplier B", "body": {"square": 20}, "movement": {"wheels": 10}},
        {"name": "Supplier C", "power": {"solar": 5}}
    ]

    # Simulate two factories with the same seed (not implemented in the test; this is a placeholder)
    quote1 = quote_robot(suppliers, {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    purchase1 = purchase_robot(quote1, suppliers)

    quote2 = quote_robot(suppliers, {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    purchase2 = purchase_robot(quote2, suppliers)

    assert purchase1['serial_name'] == purchase2['serial_name']  # Ensure names are the same if seeded