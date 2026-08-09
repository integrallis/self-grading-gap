# your complete test file
import pytest
from solution import register_suppliers, quote_robot, validate_configuration, purchase_robot

# US-1: Registering a healthy supplier pool

def test_register_suppliers_rejects_zero_suppliers():
    # Expect rejection due to fewer than 3 suppliers
    with pytest.raises(Exception) as excinfo:
        register_suppliers([])
    assert str(excinfo.value) == "at least 3 suppliers are required, got 0"

def test_register_suppliers_rejects_one_supplier():
    # Expect rejection due to fewer than 3 suppliers
    with pytest.raises(Exception) as excinfo:
        register_suppliers(["Supplier A"])
    assert str(excinfo.value) == "at least 3 suppliers are required, got 1"

def test_register_suppliers_rejects_fewer_than_three():
    # Expect rejection due to fewer than 3 suppliers
    with pytest.raises(Exception) as excinfo:
        register_suppliers(["Supplier A", "Supplier B"])
    assert str(excinfo.value) == "at least 3 suppliers are required, got 2"

def test_register_suppliers_rejects_duplicate_names():
    # Expect rejection due to duplicate supplier name
    with pytest.raises(Exception) as excinfo:
        register_suppliers(["Supplier A", "Supplier B", "Supplier A"])
    assert str(excinfo.value) == "duplicate supplier name Supplier A"


# US-2: Quoting a robot at the lowest cost

def test_quote_robot_lowest_cost_per_category():
    register_suppliers([
        "Supplier A",
        "Supplier B",
        "Supplier C"
    ])
    
    quote = quote_robot({
        "head": "standard vision",
        "body": "square",
        "arms": "hands",
        "movement": "wheels",
        "power": "solar"
    })
    
    # Expected quote based on lowest prices from suppliers
    expected_quote = {
        "head": ("Supplier A", 50),
        "body": ("Supplier B", 90),
        "arms": ("Supplier B", 25),
        "movement": ("Supplier A", 20),
        "power": ("Supplier A", 10)
    }
    assert quote['parts'] == expected_quote
    assert quote['total'] == 195  # Total = 50 + 90 + 25 + 20 + 10

def test_quote_robot_with_tie_breaker():
    register_suppliers([
        "Supplier A",
        "Supplier B",
        "Supplier C"
    ])
    
    quote = quote_robot({"head": "standard vision"})
    
    # Supplier A should win due to being registered first
    expected_quote = {
        "head": ("Supplier A", 50)  # Supplier A registered first
    }
    assert quote['parts'] == expected_quote

def test_quote_robot_with_split_sourcing():
    register_suppliers([
        "Supplier A",
        "Supplier B",
        "Supplier C"
    ])
    
    quote = quote_robot({
        "head": "standard vision",
        "body": "square",
        "arms": "hands",
        "movement": "wheels",
        "power": "solar"
    })
    
    # Expected quote based on available suppliers
    expected_quote = {
        "head": ("Supplier A", 50),
        "body": ("Supplier A", 100),
        "arms": ("Supplier B", 25),
        "movement": ("Supplier B", 20),
        "power": ("Supplier C", 10)
    }
    assert quote['parts'] == expected_quote
    assert quote['total'] == 205  # Total = 50 + 100 + 25 + 20 + 10

# US-3: Validating robot configurations

def test_validate_configuration_missing_head():
    with pytest.raises(Exception) as excinfo:
        validate_configuration({"body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    assert str(excinfo.value) == "missing part category head"

def test_validate_configuration_missing_body():
    with pytest.raises(Exception) as excinfo:
        validate_configuration({"head": "standard vision", "arms": "hands", "movement": "wheels", "power": "solar"})
    assert str(excinfo.value) == "missing part category body"

def test_validate_configuration_missing_arms():
    with pytest.raises(Exception) as excinfo:
        validate_configuration({"head": "standard vision", "body": "square", "movement": "wheels", "power": "solar"})
    assert str(excinfo.value) == "missing part category arms"

def test_validate_configuration_missing_movement():
    with pytest.raises(Exception) as excinfo:
        validate_configuration({"head": "standard vision", "body": "square", "arms": "hands", "power": "solar"})
    assert str(excinfo.value) == "missing part category movement"

def test_validate_configuration_missing_power():
    with pytest.raises(Exception) as excinfo:
        validate_configuration({"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels"})
    assert str(excinfo.value) == "missing part category power"

def test_validate_configuration_unknown_part_category():
    with pytest.raises(Exception) as excinfo:
        validate_configuration({"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar", "wings": "none"})
    assert str(excinfo.value) == "unknown part category wings"

def test_validate_configuration_invalid_head_option():
    with pytest.raises(Exception) as excinfo:
        validate_configuration({"head": "nonexistent option", "body": "square", "arms": "hands", "movement": "wheels", "power": "solar"})
    assert str(excinfo.value) == "invalid head option nonexistent option"

def test_validate_configuration_invalid_body_option():
    with pytest.raises(Exception) as excinfo:
        validate_configuration({"head": "standard vision", "body": "nonexistent option", "arms": "hands", "movement": "wheels", "power": "solar"})
    assert str(excinfo.value) == "invalid body option nonexistent option"

def test_validate_configuration_invalid_arms_option():
    with pytest.raises(Exception) as excinfo:
        validate_configuration({"head": "standard vision", "body": "square", "arms": "nonexistent option", "movement": "wheels", "power": "solar"})
    assert str(excinfo.value) == "invalid arms option nonexistent option"

def test_validate_configuration_invalid_movement_option():
    with pytest.raises(Exception) as excinfo:
        validate_configuration({"head": "standard vision", "body": "square", "arms": "hands", "movement": "nonexistent option", "power": "solar"})
    assert str(excinfo.value) == "invalid movement option nonexistent option"

def test_validate_configuration_invalid_power_option():
    with pytest.raises(Exception) as excinfo:
        validate_configuration({"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "nonexistent option"})
    assert str(excinfo.value) == "invalid power option nonexistent option"

def test_validate_configuration_no_supplier_carries_option():
    register_suppliers([
        "Supplier A",
        "Supplier B",
        "Supplier C"
    ])
    with pytest.raises(Exception) as excinfo:
        validate_configuration({"head": "standard vision", "body": "square", "arms": "hands", "movement": "wheels", "power": "biomass"})
    assert str(excinfo.value) == "no supplier carries biomass"


# US-4: Purchasing robots and tracking supplier orders

def test_purchase_robot_records_orders():
    register_suppliers([
        "Supplier A",
        "Supplier B",
        "Supplier C"
    ])
    
    quote = quote_robot({
        "head": "standard vision",
        "body": "square",
        "arms": "hands",
        "movement": "wheels",
        "power": "solar"
    })
    purchase = purchase_robot(quote)
    
    # Check that the purchase records correct orders
    assert purchase['total'] == quote['total']
    assert purchase['orders'] == [
        {"supplier": "Supplier A", "parts": {"head": "standard vision", "price": 50}, "total": 50},
        {"supplier": "Supplier B", "parts": {"body": "square", "price": 90, "arms": "hands", "price": 25}, "total": 115},
        {"supplier": "Supplier A", "parts": {"movement": "wheels", "price": 20}, "total": 20},
        {"supplier": "Supplier A", "parts": {"power": "solar", "price": 10}, "total": 10}
    ]

def test_purchase_robot_no_orders_on_quote():
    register_suppliers([
        "Supplier A",
        "Supplier B",
        "Supplier C"
    ])
    
    quote = quote_robot({
        "head": "standard vision",
        "body": "square",
        "arms": "hands",
        "movement": "wheels",
        "power": "solar"
    })
    
    # Ensure that no orders are recorded before purchase
    assert quote['orders'] == []

def test_purchase_robot_unknown_supplier():
    with pytest.raises(Exception) as excinfo:
        purchase_robot({"supplier": "unknown supplier"})
    assert str(excinfo.value) == "unknown supplier unknown supplier"