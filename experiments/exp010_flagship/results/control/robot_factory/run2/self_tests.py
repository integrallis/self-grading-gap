import pytest
from solution import register_suppliers, quote_robot, validate_configuration, purchase_robot, get_order_history

def test_register_suppliers_rejects_fewer_than_three_suppliers():
    with pytest.raises(ValueError) as excinfo:
        register_suppliers(["Supplier A", "Supplier B"])
    assert str(excinfo.value) == "at least 3 suppliers are required, got 2"

def test_register_suppliers_rejects_duplicate_supplier_names():
    with pytest.raises(ValueError) as excinfo:
        register_suppliers(["Supplier A", "Supplier A", "Supplier B"])
    assert str(excinfo.value) == "duplicate supplier name Supplier A"

def test_quote_robot_sources_parts_from_cheapest_suppliers():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}, "arms": {"hands": 5}, "movement": {"wheels": 15}, "power": {"solar": 30}}),
        ("Supplier B", {"head": {"standard vision": 8}, "body": {"square": 25}, "arms": {"hands": 3}, "movement": {"wheels": 15}, "power": {"solar": 35}}),
        ("Supplier C", {"head": {"standard vision": 10}, "body": {"square": 20}, "arms": {"hands": 5}, "movement": {"wheels": 14}, "power": {"solar": 30}}),
    ]
    register_suppliers(suppliers)
    
    quote = quote_robot({"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    
    # Expected parts: head from Supplier B (8), body from Supplier A (20), arms from Supplier B (3), movement from Supplier C (14), power from Supplier A (30)
    expected_parts = [
        {"category": "head", "supplier": "Supplier B", "price": 8},
        {"category": "body", "supplier": "Supplier A", "price": 20},
        {"category": "arms", "supplier": "Supplier B", "price": 3},
        {"category": "movement", "supplier": "Supplier C", "price": 14},
        {"category": "power", "supplier": "Supplier A", "price": 30},
    ]
    expected_total = 8 + 20 + 3 + 14 + 30  # 75
    
    assert quote["parts"] == expected_parts
    assert quote["total"] == expected_total

def test_quote_robot_ties_on_price_picks_first_supplier():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}, "arms": {"hands": 5}, "movement": {"wheels": 15}, "power": {"solar": 30}}),
        ("Supplier B", {"head": {"standard vision": 10}, "body": {"square": 25}, "arms": {"hands": 3}, "movement": {"wheels": 15}, "power": {"solar": 35}}),
    ]
    register_suppliers(suppliers)
    
    quote = quote_robot({"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    
    # Expected parts: head from Supplier A (10), body from Supplier A (20), arms from Supplier B (3), movement from Supplier A (15), power from Supplier A (30)
    expected_parts = [
        {"category": "head", "supplier": "Supplier A", "price": 10},
        {"category": "body", "supplier": "Supplier A", "price": 20},
        {"category": "arms", "supplier": "Supplier B", "price": 3},
        {"category": "movement", "supplier": "Supplier A", "price": 15},
        {"category": "power", "supplier": "Supplier A", "price": 30},
    ]
    expected_total = 10 + 20 + 3 + 15 + 30  # 78
    
    assert quote["parts"] == expected_parts
    assert quote["total"] == expected_total

def test_validate_configuration_rejects_missing_part_category():
    with pytest.raises(ValueError) as excinfo:
        validate_configuration({"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels"})
    assert str(excinfo.value) == "missing part category power"

def test_validate_configuration_rejects_unknown_part_category():
    with pytest.raises(ValueError) as excinfo:
        validate_configuration({"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar", "extra": "value"})
    assert str(excinfo.value) == "unknown part category extra"

def test_validate_configuration_rejects_invalid_option():
    with pytest.raises(ValueError) as excinfo:
        validate_configuration({"head": "invalid option", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    assert str(excinfo.value) == "invalid head option invalid option"

def test_validate_configuration_rejects_unavailable_supplier_option():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}, "arms": {"hands": 5}, "movement": {"wheels": 15}, "power": {"solar": 30}}),
        ("Supplier B", {"head": {"infrared vision": 8}, "body": {"square": 25}, "arms": {"hands": 3}, "movement": {"wheels": 15}, "power": {"solar": 35}}),
    ]
    register_suppliers(suppliers)
    
    with pytest.raises(ValueError) as excinfo:
        validate_configuration({"head": "night vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    assert str(excinfo.value) == "no supplier carries night vision"

def test_purchase_robot_records_supplier_orders():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}, "arms": {"hands": 5}, "movement": {"wheels": 15}, "power": {"solar": 30}}),
        ("Supplier B", {"head": {"standard vision": 8}, "body": {"square": 25}, "arms": {"hands": 3}, "movement": {"wheels": 15}, "power": {"solar": 35}}),
        ("Supplier C", {"head": {"standard vision": 10}, "body": {"square": 20}, "arms": {"hands": 5}, "movement": {"wheels": 14}, "power": {"solar": 30}}),
    ]
    register_suppliers(suppliers)
    
    quote = quote_robot({"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    purchase_robot(quote)
    
    order_history_a = get_order_history("Supplier A")
    order_history_b = get_order_history("Supplier B")
    order_history_c = get_order_history("Supplier C")
    
    # Supplier A: body (20), power (30)
    expected_a = [
        {"category": "body", "option": "square", "price": 20},
        {"category": "power", "option": "solar", "price": 30},
    ]
    
    # Supplier B: head (8), arms (3)
    expected_b = [
        {"category": "head", "option": "standard vision", "price": 8},
        {"category": "arms", "option": "hands", "price": 5},
    ]
    
    # Supplier C: movement (14)
    expected_c = [
        {"category": "movement", "option": "wheels", "price": 14},
    ]
    
    assert order_history_a == expected_a
    assert order_history_b == expected_b
    assert order_history_c == expected_c

def test_get_order_history_rejects_unknown_supplier():
    with pytest.raises(ValueError) as excinfo:
        get_order_history("Unknown Supplier")
    assert str(excinfo.value) == "unknown supplier Unknown Supplier"

def test_purchase_robot_matches_quote_parts_and_total():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}, "arms": {"hands": 5}, "movement": {"wheels": 15}, "power": {"solar": 30}}),
        ("Supplier B", {"head": {"standard vision": 8}, "body": {"square": 25}, "arms": {"hands": 3}, "movement": {"wheels": 15}, "power": {"solar": 35}}),
    ]
    register_suppliers(suppliers)
    
    quote = quote_robot({"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    purchase_robot(quote)
    
    # The quote should match the purchase
    assert quote["parts"] == purchase_robot(quote)["parts"]
    assert quote["total"] == purchase_robot(quote)["total"]

def test_robot_serial_name_format():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}, "arms": {"hands": 5}, "movement": {"wheels": 15}, "power": {"solar": 30}}),
        ("Supplier B", {"head": {"standard vision": 8}, "body": {"square": 25}, "arms": {"hands": 3}, "movement": {"wheels": 15}, "power": {"solar": 35}}),
    ]
    register_suppliers(suppliers)
    
    quote = quote_robot({"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    purchased_robot = purchase_robot(quote)
    
    # Checking the serial name format
    serial_name = purchased_robot["serial_name"]  # Assuming the purchase_robot returns the robot with serial name
    
    assert len(serial_name) == 5
    assert serial_name[:2].isupper()  # First two characters are uppercase letters
    assert serial_name[2:].isdigit()  # Last three characters are digits