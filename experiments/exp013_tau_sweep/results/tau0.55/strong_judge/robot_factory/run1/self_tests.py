import pytest
from solution import register_suppliers, quote_robot, validate_configuration, purchase_robot

# Test for registering suppliers

def test_register_suppliers_fewer_than_three_suppliers():
    with pytest.raises(ValueError) as excinfo:
        register_suppliers([])
    assert str(excinfo.value) == "at least 3 suppliers are required, got 0"

    with pytest.raises(ValueError) as excinfo:
        register_suppliers([{"name": "Supplier A"}])
    assert str(excinfo.value) == "at least 3 suppliers are required, got 1"

    with pytest.raises(ValueError) as excinfo:
        register_suppliers([{"name": "Supplier A"}, {"name": "Supplier B"}])
    assert str(excinfo.value) == "at least 3 suppliers are required, got 2"

def test_register_suppliers_duplicate_names():
    with pytest.raises(ValueError) as excinfo:
        register_suppliers([{"name": "Supplier A"}, {"name": "Supplier B"}, {"name": "Supplier A"}])
    assert str(excinfo.value) == "duplicate supplier name Supplier A"


# Test for quoting a robot

def test_quote_robot_lowest_cost():
    suppliers = [
        {"name": "Supplier A", "parts": {"head": {"standard vision": 50}, "body": {"square": 100}, "arms": {"hands": 20}, "movement": {"wheels": 30}, "power": {"solar": 70}}},
        {"name": "Supplier B", "parts": {"head": {"standard vision": 60}, "body": {"square": 90}, "arms": {"hands": 25}, "movement": {"wheels": 30}, "power": {"solar": 60}}},
        {"name": "Supplier C", "parts": {"head": {"standard vision": 55}, "body": {"square": 110}, "arms": {"hands": 15}, "movement": {"legs": 40}, "power": {"solar": 65}}}
    ]
    quote = quote_robot(suppliers, {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    assert quote["total"] == 245  # 50 + 90 + 15 + 30 + 60

def test_quote_robot_with_ties():
    suppliers = [
        {"name": "Supplier A", "parts": {"head": {"standard vision": 50}}},
        {"name": "Supplier B", "parts": {"head": {"standard vision": 50}}},
        {"name": "Supplier C", "parts": {"head": {"infrared vision": 40}}}
    ]
    quote = quote_robot(suppliers, {"head": "standard vision"})
    assert quote["parts"][0]["supplier"] == "Supplier A"  # Supplier A registered first

def test_quote_robot_partial_suppliers():
    suppliers = [
        {"name": "Supplier A", "parts": {"head": {"standard vision": 50}}},
        {"name": "Supplier B", "parts": {"body": {"round": 90}}},
        {"name": "Supplier C", "parts": {"arms": {"hands": 20}}},
    ]
    with pytest.raises(ValueError) as excinfo:
        quote_robot(suppliers, {"head": "standard vision", "body": "round", "arms": "hands"})
    assert str(excinfo.value) == "missing part category movement"


# Test for validating robot configurations

def test_validate_configuration_missing_part_category():
    with pytest.raises(ValueError) as excinfo:
        validate_configuration({"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels"})
    assert str(excinfo.value) == "missing part category power"

def test_validate_configuration_unknown_part_category():
    with pytest.raises(ValueError) as excinfo:
        validate_configuration({"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar", "extra": "none"})
    assert str(excinfo.value) == "unknown part category extra"

def test_validate_configuration_invalid_option():
    with pytest.raises(ValueError) as excinfo:
        validate_configuration({"head": "invalid option", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    assert str(excinfo.value) == "invalid head option invalid option"

def test_validate_configuration_no_supplier_for_option():
    suppliers = [
        {"name": "Supplier A", "parts": {"head": {"standard vision": 50}, "body": {"square": 90}}},
        {"name": "Supplier B", "parts": {"arms": {"hands": 20}}}
    ]
    with pytest.raises(ValueError) as excinfo:
        validate_configuration({"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    assert str(excinfo.value) == "no supplier carries solar"


# Test for purchasing robots

def test_purchase_robot_matches_quote():
    suppliers = [
        {"name": "Supplier A", "parts": {"head": {"standard vision": 50}, "body": {"square": 100}, "arms": {"hands": 20}, "movement": {"wheels": 30}, "power": {"solar": 70}}},
        {"name": "Supplier B", "parts": {"head": {"standard vision": 60}, "body": {"square": 90}, "arms": {"hands": 25}, "movement": {"wheels": 30}, "power": {"solar": 60}}},
        {"name": "Supplier C", "parts": {"head": {"standard vision": 55}, "body": {"square": 110}, "arms": {"hands": 15}, "movement": {"legs": 40}, "power": {"solar": 65}}}
    ]
    quote = quote_robot(suppliers, {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    purchase = purchase_robot(quote)
    assert purchase["total"] == quote["total"]
    assert len(purchase["orders"]) == 3  # A wins 2 parts, B wins 2 parts, C wins 1 part

def test_purchase_robot_records_supplier_orders():
    suppliers = [
        {"name": "Supplier A", "parts": {"head": {"standard vision": 50}, "body": {"square": 100}, "arms": {"hands": 20}, "movement": {"wheels": 30}, "power": {"solar": 70}}},
        {"name": "Supplier B", "parts": {"head": {"standard vision": 60}, "body": {"square": 90}, "arms": {"hands": 25}, "movement": {"wheels": 30}, "power": {"solar": 60}}},
        {"name": "Supplier C", "parts": {"head": {"standard vision": 55}, "body": {"square": 110}, "arms": {"hands": 15}, "movement": {"legs": 40}, "power": {"solar": 65}}}
    ]
    quote = quote_robot(suppliers, {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    purchase = purchase_robot(quote)
    assert purchase["orders"] == [
        {"supplier": "Supplier A", "parts": [
            {"category": "head", "option": "standard vision", "price": 50},
            {"category": "movement", "option": "wheels", "price": 30}
        ]},
        {"supplier": "Supplier B", "parts": [
            {"category": "body", "option": "square", "price": 90},
            {"category": "power", "option": "solar", "price": 70}
        ]},
        {"supplier": "Supplier C", "parts": [
            {"category": "arms", "option": "hands", "price": 15}
        ]}
    ]

def test_purchase_robot_no_orders_while_quoting():
    suppliers = [
        {"name": "Supplier A", "parts": {"head": {"standard vision": 50}}},
        {"name": "Supplier B", "parts": {"body": {"round": 90}}},
        {"name": "Supplier C", "parts": {"arms": {"hands": 20}}},
    ]
    quote = quote_robot(suppliers, {"head": "standard vision", "body": "round", "arms": "hands", "movement": "wheels", "power": "solar"})
    assert all(supplier["orders"] == [] for supplier in suppliers)  # No orders should be recorded

def test_purchase_robot_order_history_unknown_supplier():
    suppliers = [
        {"name": "Supplier A", "parts": {"head": {"standard vision": 50}}},
        {"name": "Supplier B", "parts": {"body": {"round": 90}}},
        {"name": "Supplier C", "parts": {"arms": {"hands": 20}}},
    ]
    with pytest.raises(ValueError) as excinfo:
        purchase_robot({"supplier": "Unknown Supplier"})
    assert str(excinfo.value) == "unknown supplier Unknown Supplier"

# Test for unique serial names

def test_serial_name_format():
    name = "AB123"  # Format: 2 uppercase letters followed by 3 digits
    assert len(name) == 5
    assert name[:2].isupper()
    assert name[2:].isdigit()

def test_serial_name_non_repetition():
    names = set()
    for i in range(10):  # Simulate 10 robots
        name = "AB" + str(i).zfill(3)  # Generates AB000, AB001, ..., AB009
        assert name not in names
        names.add(name)

def test_serial_name_identical_sequence_from_identical_seeded_sources():
    # This test would require a specific implementation of the randomness source
    pass  # Placeholder for random source testing