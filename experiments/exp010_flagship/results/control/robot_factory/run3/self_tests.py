# test_solution.py

from solution import register_suppliers, quote_robot, validate_configuration, purchase_robot

def test_register_suppliers_rejects_fewer_than_three_suppliers():
    suppliers = [("Supplier A", {}), ("Supplier B", {})]  # 2 suppliers
    with pytest.raises(ValueError, match="at least 3 suppliers are required, got 2"):
        register_suppliers(suppliers)

def test_register_suppliers_rejects_duplicate_supplier_names():
    suppliers = [("Supplier A", {}), ("Supplier A", {})]  # Duplicate name
    with pytest.raises(ValueError, match="duplicate supplier name Supplier A"):
        register_suppliers(suppliers)

def test_quote_robot_sources_parts_from_lowest_price_supplier():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 100}, "body": {"square": 200}, "arms": {"hands": 50}}),
        ("Supplier B", {"head": {"standard vision": 90}, "body": {"square": 210}, "arms": {"hands": 40}}),
    ]
    quote = quote_robot(suppliers, {"head": "standard vision", "body": "square", "arms": "hands"})
    # Expected part sources: head from Supplier B at 90, body from Supplier A at 200, arms from Supplier B at 40
    expected_parts = [
        {"category": "head", "supplier": "Supplier B", "price": 90},
        {"category": "body", "supplier": "Supplier A", "price": 200},
        {"category": "arms", "supplier": "Supplier B", "price": 40},
    ]
    assert quote["parts"] == expected_parts
    assert quote["total"] == 330  # 90 + 200 + 40

def test_quote_robot_handles_supplier_tie_on_price():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 100}}),
        ("Supplier B", {"head": {"standard vision": 100}}),  # Tie on head price
    ]
    quote = quote_robot(suppliers, {"head": "standard vision"})
    # Expected: Supplier A should win due to first registration
    expected_parts = [{"category": "head", "supplier": "Supplier A", "price": 100}]
    assert quote["parts"] == expected_parts

def test_quote_robot_allows_missing_parts_from_suppliers():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 100}}),
        ("Supplier B", {"body": {"square": 200}}),
    ]
    quote = quote_robot(suppliers, {"head": "standard vision", "body": "square"})
    # Expected parts sourced: head from Supplier A at 100, body from Supplier B at 200
    expected_parts = [
        {"category": "head", "supplier": "Supplier A", "price": 100},
        {"category": "body", "supplier": "Supplier B", "price": 200},
    ]
    assert quote["parts"] == expected_parts
    assert quote["total"] == 300  # 100 + 200

def test_validate_configuration_rejects_missing_part_category():
    config = {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels"}  # Missing power
    with pytest.raises(ValueError, match="missing part category power"):
        validate_configuration(config)

def test_validate_configuration_rejects_unknown_part_category():
    config = {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar", "wings": "none"}  # Unknown category "wings"
    with pytest.raises(ValueError, match="unknown part category wings"):
        validate_configuration(config)

def test_validate_configuration_rejects_invalid_option():
    config = {"head": "invalid option", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"}
    with pytest.raises(ValueError, match="invalid head option invalid option"):
        validate_configuration(config)

def test_validate_configuration_rejects_unavailable_option():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 100}, "body": {"square": 200}}),
    ]
    config = {"head": "infrared vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"}
    with pytest.raises(ValueError, match="no supplier carries infrared vision"):
        validate_configuration(config)

def test_purchase_robot_records_orders_with_suppliers():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 100}, "body": {"square": 200}}),
        ("Supplier B", {"arms": {"hands": 50}, "movement": {"wheels": 75}, "power": {"solar": 150}}),
    ]
    quote = quote_robot(suppliers, {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    purchase = purchase_robot(quote)
    expected_orders = {
        "Supplier A": [{"option": "standard vision", "price": 100, "category": "head"},
                       {"option": "square", "price": 200, "category": "body"}],
        "Supplier B": [{"option": "hands", "price": 50, "category": "arms"},
                       {"option": "wheels", "price": 75, "category": "movement"},
                       {"option": "solar", "price": 150, "category": "power"}],
    }
    assert purchase["orders"] == expected_orders

def test_purchase_robot_records_same_parts_as_quote():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 100}, "body": {"square": 200}}),
        ("Supplier B", {"arms": {"hands": 50}, "movement": {"wheels": 75}, "power": {"solar": 150}}),
    ]
    quote = quote_robot(suppliers, {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    purchase = purchase_robot(quote)
    assert purchase["total"] == quote["total"]
    assert purchase["parts"] == quote["parts"]

def test_purchase_robot_rejects_unknown_supplier_order_history():
    with pytest.raises(ValueError, match="unknown supplier Unknown Supplier"):
        purchase_robot("Unknown Supplier")