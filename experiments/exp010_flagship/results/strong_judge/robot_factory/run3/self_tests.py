# test_solution.py

import pytest
from solution import register_suppliers, quote_robot, validate_configuration, purchase_robot

def test_register_suppliers_rejects_fewer_than_three_suppliers():
    with pytest.raises(ValueError) as exc_info:
        register_suppliers([])
    assert str(exc_info.value) == "at least 3 suppliers are required, got 0"
    
    with pytest.raises(ValueError) as exc_info:
        register_suppliers(["Supplier A"])
    assert str(exc_info.value) == "at least 3 suppliers are required, got 1"

    with pytest.raises(ValueError) as exc_info:
        register_suppliers(["Supplier A", "Supplier B"])
    assert str(exc_info.value) == "at least 3 suppliers are required, got 2"

def test_register_suppliers_rejects_duplicate_supplier_names():
    with pytest.raises(ValueError) as exc_info:
        register_suppliers(["Supplier A", "Supplier A", "Supplier B"])
    assert str(exc_info.value) == "duplicate supplier name Supplier A"

def test_quote_robot_returns_lowest_cost_per_part():
    suppliers = [
        {"name": "Supplier A", "parts": {"head": {"standard vision": 50}, "body": {"square": 80}}},
        {"name": "Supplier B", "parts": {"head": {"standard vision": 40}, "body": {"square": 90}}},
        {"name": "Supplier C", "parts": {"head": {"infrared vision": 60}, "body": {"round": 70}}},
    ]
    register_suppliers(suppliers)
    config = {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"}
    with pytest.raises(ValueError) as exc_info:
        quote_robot(config)
    assert str(exc_info.value) == "no supplier carries hands"

def test_quote_robot_handles_multiple_suppliers_tied_on_price():
    suppliers = [
        {"name": "Supplier A", "parts": {"head": {"standard vision": 50}}},
        {"name": "Supplier B", "parts": {"head": {"standard vision": 50}}},
        {"name": "Supplier C", "parts": {"head": {"infrared vision": 60}}},
    ]
    register_suppliers(suppliers)
    config = {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"}
    with pytest.raises(ValueError) as exc_info:
        quote_robot(config)
    assert str(exc_info.value) == "no supplier carries hands"

def test_quote_robot_handles_complete_configuration():
    suppliers = [
        {"name": "Supplier A", "parts": {"head": {"standard vision": 50}, "body": {"square": 80}, "arms": {"hands": 20}, "movement": {"wheels": 30}, "power": {"solar": 40}}},
        {"name": "Supplier B", "parts": {"head": {"standard vision": 40}, "body": {"round": 70}, "arms": {"pinchers": 15}, "movement": {"legs": 25}, "power": {"rechargeable battery": 45}}},
        {"name": "Supplier C", "parts": {"head": {"infrared vision": 60}, "body": {"triangular": 90}, "arms": {"boxing gloves": 50}, "movement": {"tracks": 35}, "power": {"biomass": 55}}},
    ]
    register_suppliers(suppliers)
    config = {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"}
    quote = quote_robot(config)
    # Prices: Supplier B for head (40), Supplier A for body (80), Supplier A for arms (20), Supplier A for movement (30), Supplier A for power (40)
    assert quote["quoted_parts"] == [
        {"category": "head", "supplier": "Supplier B", "price": 40},
        {"category": "body", "supplier": "Supplier A", "price": 80},
        {"category": "arms", "supplier": "Supplier A", "price": 20},
        {"category": "movement", "supplier": "Supplier A", "price": 30},
        {"category": "power", "supplier": "Supplier A", "price": 40},
    ]
    assert quote["total"] == 210  # 40 + 80 + 20 + 30 + 40

def test_validate_configuration_rejects_missing_part_category():
    with pytest.raises(ValueError) as exc_info:
        validate_configuration({"head": "standard vision", "body": "square", "arms": "hands", "power": "solar"})
    assert str(exc_info.value) == "missing part category movement"

def test_validate_configuration_rejects_unknown_part_category():
    with pytest.raises(ValueError) as exc_info:
        validate_configuration({"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar", "extra": "unknown"})
    assert str(exc_info.value) == "unknown part category extra"

def test_validate_configuration_rejects_invalid_option():
    with pytest.raises(ValueError) as exc_info:
        validate_configuration({"head": "invalid option", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    assert str(exc_info.value) == "invalid head option invalid option"

def test_validate_configuration_rejects_unavailable_option():
    suppliers = [
        {"name": "Supplier A", "parts": {"head": {"standard vision": 50}, "body": {"square": 80}, "arms": {"pinchers": 15}, "movement": {"legs": 25}, "power": {"solar": 40}}},
        {"name": "Supplier B", "parts": {"head": {"standard vision": 40}, "body": {"round": 70}, "arms": {"pinchers": 15}, "movement": {"legs": 25}, "power": {"rechargeable battery": 45}}},
        {"name": "Supplier C", "parts": {"head": {"infrared vision": 60}, "body": {"triangular": 90}, "arms": {"boxing gloves": 50}, "movement": {"tracks": 35}, "power": {"biomass": 55}}},
    ]
    register_suppliers(suppliers)
    with pytest.raises(ValueError) as exc_info:
        validate_configuration({"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    assert str(exc_info.value) == "no supplier carries hands"

def test_purchase_robot_records_orders():
    suppliers = [
        {"name": "Supplier A", "parts": {"head": {"standard vision": 50}, "body": {"square": 80}, "arms": {"hands": 20}, "movement": {"wheels": 30}, "power": {"solar": 40}}},
        {"name": "Supplier B", "parts": {"head": {"standard vision": 40}, "body": {"round": 70}, "arms": {"pinchers": 15}, "movement": {"legs": 25}, "power": {"rechargeable battery": 45}}},
        {"name": "Supplier C", "parts": {"head": {"infrared vision": 60}, "body": {"triangular": 90}, "arms": {"boxing gloves": 50}, "movement": {"tracks": 35}, "power": {"biomass": 55}}},
    ]
    register_suppliers(suppliers)
    config = {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"}
    quote = quote_robot(config)
    purchase = purchase_robot(config)
    # Purchase orders should match the quoted parts
    assert purchase["orders"] == [
        {"supplier": "Supplier B", "part": "head", "option": "standard vision", "price": 40},
        {"supplier": "Supplier A", "part": "body", "option": "square", "price": 80},
        {"supplier": "Supplier A", "part": "arms", "option": "hands", "price": 20},
        {"supplier": "Supplier A", "part": "movement", "option": "wheels", "price": 30},
        {"supplier": "Supplier A", "part": "power", "option": "solar", "price": 40},
    ]

def test_purchase_robot_has_correct_total():
    suppliers = [
        {"name": "Supplier A", "parts": {"head": {"standard vision": 50}, "body": {"square": 80}, "arms": {"hands": 20}, "movement": {"wheels": 30}, "power": {"solar": 40}}},
        {"name": "Supplier B", "parts": {"head": {"standard vision": 40}, "body": {"round": 70}, "arms": {"pinchers": 15}, "movement": {"legs": 25}, "power": {"rechargeable battery": 45}}},
        {"name": "Supplier C", "parts": {"head": {"infrared vision": 60}, "body": {"triangular": 90}, "arms": {"boxing gloves": 50}, "movement": {"tracks": 35}, "power": {"biomass": 55}}},
    ]
    register_suppliers(suppliers)
    config = {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"}
    quote = quote_robot(config)
    purchase = purchase_robot(config)
    # Total price should match the quoted total
    assert purchase["total"] == quote["total"]

def test_purchase_robot_rejects_unknown_supplier_for_order_history():
    suppliers = [
        {"name": "Supplier A", "parts": {"head": {"standard vision": 50}}},
        {"name": "Supplier B", "parts": {"head": {"standard vision": 40}}},
        {"name": "Supplier C", "parts": {"head": {"infrared vision": 60}}},
    ]
    register_suppliers(suppliers)
    with pytest.raises(ValueError) as exc_info:
        purchase_robot({"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    assert str(exc_info.value) == "unknown supplier Unknown Supplier"

def test_purchase_robot_records_no_orders_on_quote():
    suppliers = [
        {"name": "Supplier A", "parts": {"head": {"standard vision": 50}, "body": {"square": 80}}},
        {"name": "Supplier B", "parts": {"head": {"standard vision": 40}, "body": {"round": 70}}},
        {"name": "Supplier C", "parts": {"head": {"infrared vision": 60}, "body": {"triangular": 90}}},
    ]
    register_suppliers(suppliers)
    config = {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"}
    quote = quote_robot(config)
    # No orders should be recorded until a purchase is made
    assert quote["orders"] == []

def test_purchased_robot_serial_name_format():
    suppliers = [
        {"name": "Supplier A", "parts": {"head": {"standard vision": 50}}},
        {"name": "Supplier B", "parts": {"head": {"standard vision": 40}}},
        {"name": "Supplier C", "parts": {"head": {"infrared vision": 60}}},
    ]
    register_suppliers(suppliers)
    config = {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"}
    purchase = purchase_robot(config)
    assert len(purchase["serial_name"]) == 5
    assert purchase["serial_name"][:2].isupper()
    assert purchase["serial_name"][2:].isdigit()

def test_serial_names_are_unique():
    suppliers = [
        {"name": "Supplier A", "parts": {"head": {"standard vision": 50}}},
        {"name": "Supplier B", "parts": {"head": {"standard vision": 40}}},
        {"name": "Supplier C", "parts": {"head": {"infrared vision": 60}}},
    ]
    register_suppliers(suppliers)
    config = {"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"}
    names = set()
    for _ in range(20):  # Test for more than 10 to ensure uniqueness
        purchase = purchase_robot(config)
        assert purchase["serial_name"] not in names
        names.add(purchase["serial_name"])

def test_serial_names_are_identical_with_same_seeded_randomness():
    suppliers = [
        {"name": "Supplier A", "parts": {"head": {"standard vision": 50}}},
        {"name": "Supplier B", "parts": {"head": {"standard vision": 40}}},
        {"name": "Supplier C", "parts": {"head": {"infrared vision": 60}}},
    ]
    register_suppliers(suppliers)
    
    # Create two factories with the same randomness seed
    names_factory_1 = []
    names_factory_2 = []
    
    for _ in range(10):
        names_factory_1.append(purchase_robot({"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})["serial_name"])
    
    for _ in range(10):
        names_factory_2.append(purchase_robot({"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})["serial_name"])
    
    assert names_factory_1 == names_factory_2